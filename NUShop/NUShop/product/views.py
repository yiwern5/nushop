from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg, Count
from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product, ProductImage, Variation, Review
from .forms import NewProductForm, EditProductForm, AddImageForm, ChangeImageForm, AddVariationForm, EditVariationForm, ReviewForm

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
    seller_products = Product.objects.filter(created_by=seller)
    numRating = 0
    totalRating = 0
    for seller_product in seller_products:
        numRating += seller_product.reviews.count()
        if seller_product.average_rating != None:
            totalRating += seller_product.average_rating
    if numRating != 0:
        avgRating = totalRating/numRating
    else:
        avgRating = 0

    return render(request, 'product/detail.html', {
        'avgRating': avgRating,
        'numRating': numRating,
        'reviews': reviews,
        'variations': variations,
        'images': images,
        'product': product,
        'products': products, 
        'related_products': related_products,
        'seller': seller,
        'seller_product': seller_product,
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
def edit_variation(request, variation_id, product_id):
    variation = get_object_or_404(Variation, pk=variation_id)
    product = get_object_or_404(Product, pk=product_id, created_by=request.user)
    if request.method == 'POST':
        form = EditVariationForm(request.POST, request.FILES, instance=variation)
        if form.is_valid():
            form.save()
            return redirect('product:detail', pk=product.id)
    else:
        form = EditVariationForm(instance=variation)

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
def edit_variation(request, variation_id, product_id):
    variation = get_object_or_404(Variation, pk=variation_id)
    product = get_object_or_404(Product, pk=product_id, created_by=request.user)
    if request.method == 'POST':
        form = EditVariationForm(request.POST, request.FILES, instance=variation)
        if form.is_valid():
            form.save()
            return redirect('product:detail', pk=product.id)
    else:
        form = EditVariationForm(instance=variation)

    return render(request, 'product/form.html', {
        'form': form,
        'title': f'Change options for {variation.option}'
    })

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

def some_category(request):
    club_merchandise = Category.objects.create(name = 'Club Merchandise')
    
# @login_required
# def OFF_variation(request, pk):
#     product = get_object_or_404(Product, pk=pk, created_by=request.user)
#     product.variation_bool = False
#     product.save()

#     return redirect('product:detail', pk=product.id)

# @login_required
# def ON_variation(request, pk):
#     product = get_object_or_404(Product, pk=pk, created_by=request.user)
#     product.variation_bool = True
#     product.save()
    
#     return redirect('product:detail', pk=product.id)