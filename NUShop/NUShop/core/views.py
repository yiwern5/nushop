from django.shortcuts import render, redirect
from .forms import SignupForm
from product.models import Category, Product

# Create your views here.
def index(request):
    products = Product.objects.filter(is_sold=False)
    categories = Category.objects.all()

    return render(request, 'core/index.html', {
        'categories': categories,
        'products': products,
    })

def contact(request):
    return render(request, 'core/contact.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/login/')
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