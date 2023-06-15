from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
import stripe
import time
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import UserPayment
from product.models import Product
from .models import CartProduct, Cart
from authuser.models import User
from .forms import EditDeliveryDetailsForm

# Create your views here.
@login_required
def index(request):
    products = CartProduct.objects.filter(created_by=request.user)

    return render(request, 'checkout/index.html', {
        'products': products, 
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
def payment(request):
    products = Product.objects.filter(created_by=request.user)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == 'POST':
        checkout_session = stripe.checkout.Session.create(
            payment_method_types = ['card'],
            line_items = [
                {
                    'price': settings.PRODUCT_PRICE,
                    'quantity': 1,
                },
            ],
            mode = 'payment',
            customer_creation = 'always',
            success_url = settings.REDIRECT_DOMAIN + '/payment_successful?session_id={CHECKOUT_SESSION_ID}',
            cancel_url = settings.REDIRECT_DOMAIN + '/payment_cancelled',
        )
        return redirect(checkout_session.url, code=303)
    return render(request, 'checkout/payment.html', {
        'title': 'Payment',
        'products': products,
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
            return redirect('checkout:payment')
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
            return redirect('checkout:payment')
    else:
        form = EditDeliveryDetailsForm(instance=delivery_details)

    return render(request, 'checkout/form.html', {
        'form': form,
        'title': 'Delivery Details',
    })

def payment_successful(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session_id = request.GET.get('session_id', None)
    session = stripe.checkout.Session.retrieve(checkout_session_id)
    customer = stripe.Customer.retrieve(session.customer)
    user_id = request.user.user_id
    user_payment = UserPayment.objects.get(app_user=user_id)
    user_payment.stripe_checkout_id = checkout_session_id
    user_payment.save()
    return render(request, 'user_payment/payment_successful.html', {'customer': customer})

def payment_cancelled(request):
    return render(request, 'user_payment/payment_cancelled.html')

@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    time.sleep(10)
    payload = request.body
    signature_header = request.META['HTTP_STRIPW_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, signature_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        session_id = session.get('id', None)
        time.sleep(15)
        user_payment = UserPayment.objects.get(stripe_checkout_id=session_id)
        line_items = stripe.checkout.Session.list_line_items(session_id, limit=1)
        user_payment.payment_bool = True
        user_payment.save()
    return HttpResponse(status=200)

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