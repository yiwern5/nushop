from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product, ProductImage
from .forms import NewProductForm, EditProductForm, AddImageForm, ChangeImageForm

# Create your views here.
def products(request):
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

    return render(request, 'product/products.html', {
        'products': products,
        'query': query,
        'categories': categories,
        'category_id': int(category_id),
        'category_name': category_name,
    })

def detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    images = product.images.all()
    products = Product.objects.filter(is_sold=False)[0:6]
    """
    is_sold can be changed to is_out_of_stock; 
    exclude pk=pk is to exclude this product from being shown in recommended;
    related_products can be renamed to recommendations
    [0:3] is to list 3 products
    """
    related_products = Product.objects.filter(category=product.category, is_sold=False).exclude(pk=pk)[0:3]
    seller = product.created_by
    seller_product = Product.objects.filter(created_by=seller)
    
    return render(request, 'product/detail.html', {
        'images': images,
        'product': product,
        'products': products, 
        'related_products': related_products,
        'seller': seller,
        'seller_product': seller_product
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
def deleteimage(request, image_id, product_id):
    image = get_object_or_404(ProductImage, pk=image_id, uploaded_by=request.user)
    product = get_object_or_404(Product, pk=product_id, created_by=request.user)
    image.delete()

    return redirect('product:detail', pk=product.id)

# @login_required
# def new(request):
#     if request.method == 'POST':
#         form = NewProductForm(request.POST, request.FILES)
#         if form.is_valid():
#             product = form.save(commit=False)
#             product.created_by = request.user
#             product.save()
#             form.save_m2m()  # Save the many-to-many relationships
#             return redirect('product:detail', pk=product.id)
#     else:
#         form = NewProductForm()

#     return render(request, 'product/form.html', {
#         'form': form,
#         'title': 'New product',
#     })

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
        'title': 'Edit product'
    })

@login_required
def changeimage(request, image_id, product_id):
    image = get_object_or_404(ProductImage, pk=image_id, uploaded_by=request.user)
    product = get_object_or_404(Product, pk=product_id, created_by=request.user)
    if request.method == 'POST':
        form = ChangeImageForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            form.save()
            return redirect('product:detail', pk=product.id)
    else:
        form = ChangeImageForm(instance=image)

    return render(request, 'product/form.html', {
        'form': form,
        'title': 'Change Image'
    })

@login_required
def addimage(request, pk):
    product = get_object_or_404(Product, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = AddImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.uploaded_by = request.user
            image.product = product
            image.save()
            return redirect('product:detail', pk=product.id)
    else:
        form = AddImageForm()

    return render(request, 'product/form.html', {
        'form': form,
        'title': 'Add image'
    })

# @login_required
# def edit(request, pk):
#     product = get_object_or_404(Product, pk=pk, created_by=request.user)
#     ImageFormSet = inlineformset_factory(
#         Product,
#         ProductImage,
#         form=ProductImageForm,
#         extra=1,  # Number of extra image forms
#         can_delete=True
#     )

#     if request.method == 'POST':
#         form = EditProductForm(request.POST, request.FILES, instance=product)
#         formset = ImageFormSet(request.POST, request.FILES, instance=product)
#         if form.is_valid() and formset.is_valid():
#             form.save()
#             formset.save()
#             return redirect('product:detail', pk=product.id)
#     else:
#         form = EditProductForm(instance=product)
#         formset = ImageFormSet(instance=product)

#     return render(request, 'product/form.html', {
#         'form': form,
#         'formset': formset,
#         'title': 'Edit product'
#     })