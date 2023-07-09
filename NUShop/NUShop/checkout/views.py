from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from product.models import Product, Variation, Subvariation
from .models import CartProduct, Cart
from authuser.models import User
from .forms import EditDeliveryDetailsForm
from checkout.forms import AddToCartForm
import stripe
from django.views import View
from django.views.generic import TemplateView
from django.templatetags.static import static
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse

stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        print("Payment was successful.")
        # TODO: run some custom code here

    return HttpResponse(status=200)

class CreateStripeCheckoutSessionView(View):
    """
    Create a checkout session and redirect the user to Stripe's checkout page
    """

    def post(self, request, *args, **kwargs):
        cart = Cart.objects.filter(created_by=request.user)[0]
        total_amount = cart.get_total_amount() * 100
        total_quantity = cart.get_total_quantity()

        # Generate the URL for the static image in your Django template
        image_url = request.build_absolute_uri(static('green logo.png'))
        client_reference_id=request.user.id if request.user.is_authenticated else None,
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "sgd",
                        "unit_amount": int(total_amount),
                        "product_data": {
                            "name": "NUShop Cart",
                            "description": 'Complete payment to process your order',
                            # "images": [image_url],
                        },
                    },
                    "quantity": 1,
                }
            ],
            metadata={"product_id": cart.id},
            mode="payment",
            success_url=request.build_absolute_uri('/checkout/success/'),
            cancel_url=request.build_absolute_uri('/checkout/cancel/'),
        )
        return redirect(checkout_session.url)

    
class SuccessView(TemplateView):
    template_name = "checkout/success.html"

class CancelView(TemplateView):
    template_name = "checkout/cancel.html"

# Create your views here.
@login_required
def index(request):
    products = CartProduct.objects.filter(created_by=request.user)
    cart_qs = Cart.objects.filter(created_by=request.user)

    if cart_qs:
        cart = cart_qs[0]
        return render(request, 'checkout/index.html', {
            'products': products,
            'cart': cart,
        })
    
    return render(request, 'checkout/index.html', {
            'products': products,
    })

@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    result = ''
    quantity = 1
    
    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            selected_variations = []
            selected_subvariations = []
            result = ''
            for key, value in request.POST.items():
                if key.startswith('variation_'):
                    variation_id = key.split('_')[1]
                    subvariation_id = value
                    selected_variations.append(variation_id)
                    selected_subvariations.append(subvariation_id)

            if len(selected_variations) == len(selected_subvariations) == len(product.variations.all()):
                for variation_id, subvariation_id in zip(selected_variations, selected_subvariations):
                    variation = Variation.objects.get(id=variation_id)
                    subvariation = Subvariation.objects.get(id=subvariation_id)
                    variation_type = variation.type
                    subvariation_option = subvariation.option
                    result += f'{variation_type}: {subvariation_option}; '
                # Create your model instance using the variation, subvariation, quantity, and other data as needed
            else:
                messages.error(request, "Please select all variation options.")
                return redirect('product:detail', pk=product.id)
            
            cart_product, created = CartProduct.objects.get_or_create(
                variation=result,
                created_by=request.user,
                ordered=False,
                product=product,
                quantity=quantity,
            )
            
            cart_qs = Cart.objects.filter(created_by=request.user, completed=False)
            if cart_qs.exists():
                cart = cart_qs[0]
                # check if the cart product is in the cart
                if cart_product in cart.products.all():
                    cart_product.quantity += quantity
                    cart_product.save()
                    messages.info(request, "This product quantity was updated.")
                    return redirect('product:detail', pk=product.id)
                else:
                    cart.products.add(cart_product)
                    messages.info(request, "This product was added to your cart.")
                    return redirect('product:detail', pk=product.id)
            else:
                created_at = timezone.now()
                cart = Cart.objects.create(
                    created_by=request.user,
                    created_at=created_at,
                )
                cart.products.add(cart_product)
                messages.info(request, "This product was added to your cart.")
                return redirect('product:detail', pk=product.pk)
    else:
        form = AddToCartForm()

    return render(request, 'my_template.html', {'form': form})

    
@login_required
def select_cart_product(request):
    if request.method == 'POST':
        ordered_product_pks = request.POST.getlist('ordered_products')
        cart = Cart.objects.get(created_by=request.user, completed=False)

        # Clear the current selection
        cart.products.update(ordered=False)

        # Update the selection based on the submitted form data
        cart.products.filter(pk__in=ordered_product_pks).update(ordered=True)

    return redirect('checkout:index')

@login_required
def remove_from_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart_qs = Cart.objects.filter(created_by=request.user, completed=False)
    cart = cart_qs[0]
    cart_product = CartProduct.objects.filter(
        product=product,
        created_by=request.user,
        ordered=False
    )[0]
    cart.products.remove(cart_product)
    cart_product.delete()
    messages.info(request, "This cart was removed from your cart.")
            
    return redirect("checkout:index")

@login_required
def decrease_from_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart_product = CartProduct.objects.filter(
        product=product,
        created_by=request.user,
        ordered=False
    ).first()

    if cart_product:
        cart_product.quantity -= 1
        cart_product.save()
        messages.info(request, "The quantity was decreased by 1.")

        if cart_product.quantity == 0:
            remove_from_cart(request, pk) 

    return redirect("checkout:index")


@login_required
def increase_from_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart_product = CartProduct.objects.filter(
        product=product,
        created_by=request.user,
        ordered=False
    ).first()

    if cart_product:
        cart_product.quantity += 1
        cart_product.save()
        messages.info(request, "The quantity was increased by 1.")
    else:
        messages.error(request, "This product is not in your cart.")

    return redirect("checkout:index")


@login_required
def checkout(request):
    products = CartProduct.objects.filter(created_by=request.user)
    cart_qs = Cart.objects.filter(created_by=request.user)

    if cart_qs:
        cart = cart_qs[0]
        return render(request, 'checkout/checkout.html', {
            'products': products,
            'cart': cart,
        })
    
    return render(request, 'checkout/checkout.html', {
            'products': products,
    })

@login_required
def add_shipping_details(request, username):
    if request.method == 'POST':
        form = EditDeliveryDetailsForm(request.POST, request.FILES)
        if form.is_valid():
            delivery_details = form.save(commit=False)
            request.user.delivery_address = delivery_details
            delivery_details.save()
            request.user.save()
            messages.info(request, "Delivery details are added.")
            return redirect('checkout:checkout')
    else:
        form = EditDeliveryDetailsForm()

    return render(request, 'checkout/form.html', {
        'form': form,
        'title': 'Delivery Details',
    })

@login_required
def edit_shipping_details(request, username):
    user = User.objects.get(username=username)
    delivery_details = user.delivery_address
    if request.method == 'POST':
        form = EditDeliveryDetailsForm(request.POST, request.FILES, instance=delivery_details)
        if form.is_valid():
            form.save()
            messages.info(request, "Delivery details are updated.")
            return redirect('checkout:checkout')
    else:
        form = EditDeliveryDetailsForm(instance=delivery_details)

    return render(request, 'checkout/form.html', {
        'form': form,
        'title': 'Delivery Details',
    })

