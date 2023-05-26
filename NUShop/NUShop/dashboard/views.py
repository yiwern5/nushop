from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from product.models import Category, Product

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
