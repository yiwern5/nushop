from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from product.models import Product
from . models import CartProduct, Cart

# Create your views here.
@login_required
def index(request):
    products = CartProduct.objects.filter(created_by=request.user)

    return render(request, 'cart/index.html', {
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
        if isinstance(cart_product, CartProduct):
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

    return redirect('cart:index')
