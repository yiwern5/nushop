from django.shortcuts import render
from product.models import Category, Product
# Create your views here.
def index(request):
    products = Product.objects.filter(is_sold=False)[0:6]
    categories = Category.objects.all()

    return render(request, 'core/index.html', {
        'categories': categories,
        'products': products,
    })

def contact(request):
    return render(request, 'core/contact.html')