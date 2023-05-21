from django.shortcuts import render, get_object_or_404, redirect
from . models import Product
from .forms import NewProductForm, EditProductForm
from django.contrib.auth.decorators import login_required
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

@login_required
def new(request):
    if request.method == 'POST':
        form = NewProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.save()
            return redirect('product:detail', pk=product.id)
    else:
        form = NewProductForm()

    return render(request, 'product/form.html', {
        'form': form,
        'title': 'New product',
    })
        
@login_required
def delete(request, pk):
    product = get_object_or_404(Product, pk=pk, created_by=request.user)
    product.delete()

    return redirect('dashboard:index')

@login_required
def edit(request, pk):
    product = get_object_or_404(Product, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = EditProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product:detail', pk=product.id)
    else:
        form = EditProductForm(instance=product)

    return render(request, 'product/form.html', {
        'form': form,
        'title': 'Edit product',
    })