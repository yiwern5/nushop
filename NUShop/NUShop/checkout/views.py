from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from product.models import Product
from .models import CartProduct, Cart
from authuser.models import User
from .forms import EditDeliveryDetailsForm
import stripe
from django.views import View
from django.views.generic import TemplateView
from django.templatetags.static import static

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateStripeCheckoutSessionView(View):
    """
    Create a checkout session and redirect the user to Stripe's checkout page
    """

    def post(self, request, *args, **kwargs):
        cart = Cart.objects.get(id=self.kwargs["pk"])
        total_amount = cart.get_total_amount()
        total_quantity = cart.get_total_quantity()

        # Generate the URL for the static image in your Django template
        image_url = request.build_absolute_uri(static('green logo.png'))

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "sgd",
                        "unit_amount": int(total_amount) * 100,
                        "product_data": {
                            "name": "NUShop Cart",
                            "description": 'Complete payment to process your order',
                            "images": [image_url],
                        },
                    },
                    "quantity": total_quantity,
                }
            ],
            metadata={"product_id": cart.id},
            mode="payment",
            success_url=settings.PAYMENT_SUCCESS_URL,
            cancel_url=settings.PAYMENT_CANCEL_URL,
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
    cart = Cart.objects.filter(created_by=request.user)

    return render(request, 'checkout/index.html', {
        'products': products, 
        'cart' : cart,
    })

@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart_product, created = CartProduct.objects.get_or_create(
        created_by=request.user,
        ordered=False,
        product=product,
    )
    cart_qs = Cart.objects.filter(created_by=request.user, completed=False)
    if cart_qs.exists():
        cart = cart_qs[0]
        # check if the cart product is in the cart
        if cart_product in cart.products.all():
            cart_product.quantity += 1
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
def checkout(request):
    products = Product.objects.filter(created_by=request.user)
    cart = Cart.objects.filter(created_by=request.user)
    return render(request, 'checkout/checkout.html', {
        'title': 'Checkout',
        'products': products,
        'cart': cart,
    })

@login_required
def add_shipping_details(request):
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



# @login_required
# def card_detail(request):
#     if request.method == 'POST':
#         form = CardForm(request.user, request.POST)

#         if form.is_valid():
#             form.save()
#             return redirect('core:login')
#     else:
#         form = CardForm()

#     return render(request, 'checkout/payment.html', {
#         'form': form
#     })