from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from .forms import SignupForm
from product.models import Category, Product

# Create your views here.
def index(request):
    products = Product.objects.filter(is_sold=False)
    categories = Category.objects.all()

    if not request.user.is_authenticated:
        return render(request, 'core/index.html', {
        'categories': categories,
        'products': products,
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