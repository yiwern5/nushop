from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import F, ExpressionWrapper, FloatField
from .forms import SignupForm
from product.models import Category, Product

# Create your views here.
def index(request):
    products = Product.objects.filter(is_sold=False)
    categories = Category.objects.all()
    trending = products.order_by('-number_sold')
    onsale = Product.objects.annotate(discount_percentage=ExpressionWrapper(
        (F('price') - F('discount_price')) / F('price') * 100,
        output_field=FloatField()
    )).filter(discount_percentage__gt=50).order_by('-discount_percentage')

    if not request.user.is_authenticated:
        return render(request, 'core/index.html', {
        'categories': categories,
        'products': products,
        'trending': trending,
        'onsale': onsale,
    })

    elif request.user.major:
        foryou = Product.objects.filter(is_sold=False, created_by__major__faculty_name=request.user.major.faculty_name)

        return render(request, 'core/index.html', {
            'categories': categories,
            'products': products,
            'foryou': foryou,
        })
    
    return render(request, 'core/index.html', {
        'categories': categories,
        'products': products,
        'trending': trending,
        'onsale': onsale,
    })

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect(reverse('core:login'))
    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {
        'form': form
    })

def aboutus(request):
    return render(request, 'core/aboutus.html', {
    })

def privacypolicy(request):
    return render(request, 'core/privacypolicy.html', {
    })

def tnc(request):
    return render(request, 'core/tnc.html', {
    })