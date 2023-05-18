from django.shortcuts import render, get_object_or_404
from . models import Product

# Create your views here.
def detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    """
    is_sold can be changed to is_out_of_stock; 
    exclude pk=pk is to exclude this product from being shown in recommended;
    related_products can be renamed to recommendations
    [0:3] is to list 3 products
    """
    related_products = Product.objects.filter(category=product.category, is_sold=False).exclude(pk=pk)[0:3]
    return render(request, 'product/detail.html', {
        'product': product,
        'related_products': related_products
    })