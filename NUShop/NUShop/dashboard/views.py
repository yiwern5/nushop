from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from .forms import AddressForm
from product.models import Category, Product
from dashboard.models import Address

# Create your views here.
@login_required
def index(request):
    products = Product.objects.filter(created_by=request.user)

    return render(request, 'dashboard/index.html', {
        'products': products, 
    })

def viewseller(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    category_name = ''
    categories = Category.objects.all()
    products = Product.objects.filter(is_sold=False)

    if category_id:
        products = products.filter(category_id=category_id)
        category = categories.filter(id=category_id).first()
        if category:
            category_name = category.name

    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    return render(request, 'dashboard/view-seller.html', {
        'products': products,
        'query': query,
        'categories': categories,
        'category_id': int(category_id),
        'category_name': category_name,
    })

def mypurchases(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    category_name = ''
    categories = Category.objects.all()
    products = Product.objects.filter(is_sold=False)

    if category_id:
        products = products.filter(category_id=category_id)
        category = categories.filter(id=category_id).first()
        if category:
            category_name = category.name

    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    return render(request, 'dashboard/mypurchases.html', {
        'products': products,
        'query': query,
        'categories': categories,
        'category_id': int(category_id),
        'category_name': category_name,
    })

def mysales(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    category_name = ''
    categories = Category.objects.all()
    products = Product.objects.filter(is_sold=False)

    if category_id:
        products = products.filter(category_id=category_id)
        category = categories.filter(id=category_id).first()
        if category:
            category_name = category.name

    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    return render(request, 'dashboard/mysales.html', {
        'products': products,
        'query': query,
        'categories': categories,
        'category_id': int(category_id),
        'category_name': category_name,
    })


@login_required
def cart(request):
    products = Product.objects.filter(created_by=request.user)

    return render(request, 'dashboard/cart.html', {
        'products': products, 
    })

@login_required
def payment(request):
    products = Product.objects.filter(created_by=request.user)
    if request.method == 'POST':
        form = AddressForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = AddressForm()
    return render(request, 'dashboard/payment.html', {
        'form': form,
        'title': 'Payment',
        'products': products,
    })