from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from django.urls import reverse
from product.models import Category, Product
from authuser.models import User

# Create your views here.
@login_required
def index(request):
    products = Product.objects.filter(created_by=request.user)
    user = request.user

    return render(request, 'dashboard/index.html', {
        'products': products, 
        'user': user,
    })

def viewseller(request, username):
    seller = get_object_or_404(User, username=username)
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    category_name = ''
    categories = Category.objects.all()
    products = Product.objects.filter(is_sold=False, created_by=seller)

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
        'seller': seller,
    })

def mypurchases(request):
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

    return render(request, 'dashboard/mypurchases.html', {
        'products': products,
        'query': query,
        'categories': categories,
        'category_id': int(category_id),
        'category_name': category_name,
    })

def mysales(request):
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

    return render(request, 'dashboard/mysales.html', {
        'products': products,
        'query': query,
        'categories': categories,
        'category_id': int(category_id),
        'category_name': category_name,
    })

@login_required
def follow(request, username):
    follower = request.user
    following = get_object_or_404(User, username=username)
    
    following.followers.add(follower)
    messages.info(request, "You followed this seller.")
    
    return redirect(reverse('dashboard:view-seller', args=[username]))

@login_required
def unfollow(request, username):
    follower = request.user
    following = get_object_or_404(User, username=username)
    
    following.followers.remove(follower)
    messages.info(request, "You unfollowed this seller.")
    
    return redirect(reverse('dashboard:view-seller', args=[username]))

@login_required
def viewprofile(request, username):
    user = User.objects.get(username=username)

    return render(request, 'dashboard/view-profile.html', {
        'user': user,
    })