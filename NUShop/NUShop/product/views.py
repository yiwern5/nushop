from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product, ProductImage, Variation, Subvariation, Review
from .forms import NewProductForm, EditProductForm, AddImageForm, ChangeImageForm, AddVariationForm, AddSubvariationForm, ChangeSubvariationForm, ChangeVariationForm, ReviewForm

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
    variations = product.variations.all()
    reviews = product.reviews.all()
    products = Product.objects.filter(is_sold=False)
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
        'reviews': reviews,
        'variations': variations,
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
def delete_image(request, image_id, product_id):
    image = get_object_or_404(ProductImage, pk=image_id, uploaded_by=request.user)
    product = get_object_or_404(Product, pk=product_id, created_by=request.user)
    image.delete()

    return redirect('product:detail', pk=product.id)

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
def change_image(request, image_id, product_id):
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
def add_image(request, pk):
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

@login_required
def add_variation(request, pk):
    product = get_object_or_404(Product, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = AddVariationForm(request.POST, request.FILES)
        if form.is_valid():
            variation = form.save(commit=False)
            variation.product = product
            variation.save()
            return redirect('product:detail', pk=product.id)
    else:
        form = AddVariationForm()

    return render(request, 'product/form.html', {
        'form': form,
        'title': 'Add Variation'
    })

@login_required
def change_variation(request, variation_id, product_id):
    variation = get_object_or_404(Variation, pk=variation_id)
    product = get_object_or_404(Product, pk=product_id, created_by=request.user)
    if request.method == 'POST':
        form = ChangeVariationForm(request.POST, request.FILES, instance=variation)
        if form.is_valid():
            form.save()
            return redirect('product:detail', pk=product.id)
    else:
        form = ChangeVariationForm(instance=variation)

    return render(request, 'product/form.html', {
        'form': form,
        'title': 'Change Variation'
    })

@login_required
def delete_variation(request, variation_id, product_id):
    variation = get_object_or_404(Variation, pk=variation_id)
    product = get_object_or_404(Product, pk=product_id, created_by=request.user)
    variation.delete()

    return redirect('product:detail', pk=product.id)

@login_required
def add_subvariation(request, product_id, variation_id):
    product = get_object_or_404(Product, pk=product_id, created_by=request.user)
    variation = get_object_or_404(Variation, pk=variation_id)
    if request.method == 'POST':
        form = AddSubvariationForm(request.POST, request.FILES)
        if form.is_valid():
            subvariation = form.save(commit=False)
            subvariation.variation = variation
            subvariation.save()
            return redirect('product:detail', pk=product.id)
    else:
        form = AddSubvariationForm()

    return render(request, 'product/form.html', {
        'form': form,
        'title': f'Add Options for {variation.type}'
    })

@login_required
def change_subvariation(request, subvariation_id, product_id):
    subvariation = get_object_or_404(Subvariation, pk=subvariation_id)
    product = get_object_or_404(Product, pk=product_id, created_by=request.user)
    if request.method == 'POST':
        form = ChangeSubvariationForm(request.POST, request.FILES, instance=subvariation)
        if form.is_valid():
            form.save()
            return redirect('product:detail', pk=product.id)
    else:
        form = ChangeSubvariationForm(instance=subvariation)

    return render(request, 'product/form.html', {
        'form': form,
        'title': f'Change options for {subvariation.option}'
    })

@login_required
def delete_subvariation(request, subvariation_id, product_id):
    subvariation = get_object_or_404(Subvariation, pk=subvariation_id)
    product = get_object_or_404(Product, pk=product_id, created_by=request.user)
    subvariation.delete()

    return redirect('product:detail', pk=product.id)

@login_required
def add_review(request, pk):
    product = get_object_or_404(Product, pk=pk,)
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.created_by = request.user
            review.product = product
            review.save()
            return redirect('product:detail', pk=product.id)
    else:
        form = ReviewForm()

    return render(request, 'product/form.html', {
        'form': form,
        'title': 'Add Review'
    })

@login_required
def delete_review(request, review_id, product_id):
    review = get_object_or_404(Review, pk=review_id)
    product = get_object_or_404(Product, pk=product_id, created_by=request.user)
    review.delete()

    return redirect('product:detail', pk=product.id)