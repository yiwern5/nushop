from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from django.urls import reverse
from product.models import Category, Product
from authuser.models import User, Bank, DeliveryAddress
from .forms import CustomPasswordChangeForm, EditIndividualForm, EditStudentOrganisationForm, EditBankDetailsForm, EditDeliveryDetailsForm


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
def cart(request):
    products = Product.objects.filter(created_by=request.user)

    return render(request, 'dashboard/cart.html', {
        'products': products, 
    })

@login_required
def payment(request):
    products = Product.objects.filter(created_by=request.user)
    if request.method == 'POST':
        form = AddressForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = AddressForm()
    return render(request, 'dashboard/payment.html', {
        'form': form,
        'title': 'Payment',
        'products': products,

@login_required
def follow(request, username):
    follower = request.user
    following = get_object_or_404(User, username=username)
    
    following.followers.add(follower)
    
    return redirect(reverse('dashboard:view-seller', args=[username]))

@login_required
def unfollow(request, username):
    follower = request.user
    following = get_object_or_404(User, username=username)
    
    following.followers.remove(follower)
    
    return redirect(reverse('dashboard:view-seller', args=[username]))

@login_required
def viewprofile(request, username):
    user = User.objects.get(username=username)

    return render(request, 'dashboard/view-profile.html', {
        'user': user,
    })

@login_required
def edit_individual_details(request, username):
    user = User.objects.get(username=username)
    if request.method == 'POST':
        form = EditIndividualForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect(reverse('dashboard:view-profile', args=[username]))

    else:
        form = EditIndividualForm(instance=user)

    return render(request, 'dashboard/form.html', {
        'form': form,
        'title': 'Personal Details',
    })

@login_required
def edit_student_org_details(request, username):
    user = User.objects.get(username=username)
    if request.method == 'POST':
        form = EditStudentOrganisationForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()
            return redirect(reverse('dashboard:view-profile', args=[username]))

    else:
        form = EditStudentOrganisationForm(instance=user)

    return render(request, 'dashboard/form.html', {
        'form': form,
        'title': 'Personal Details',
    })

@login_required
def edit_bank_details(request, username):
    user = User.objects.get(username=username)
    bank = user.bank_details
    if request.method == 'POST':
        form = EditBankDetailsForm(request.POST, request.FILES, instance=bank)
        if form.is_valid():
            form.save()
            return redirect(reverse('dashboard:view-profile', args=[username]))
    else:
        form = EditBankDetailsForm(instance=bank)

    return render(request, 'dashboard/form.html', {
        'form': form,
        'title': 'Bank Details',
    })


@login_required
def edit_delivery_details(request, username):
    user = User.objects.get(username=username)
    delivery_details = user.delivery_address
    if request.method == 'POST':
        form = EditDeliveryDetailsForm(request.POST, request.FILES, instance=delivery_details)
        if form.is_valid():
            form.save()
            return redirect(reverse('dashboard:view-profile', args=[username]))
    else:
        form = EditDeliveryDetailsForm(instance=delivery_details)

    return render(request, 'dashboard/form.html', {
        'form': form,
        'title': 'Delivery Details',
    })

@login_required
def add_bank_details(request, username):
    if request.method == 'POST':
        form = EditBankDetailsForm(request.POST, request.FILES)
        if form.is_valid():
            bank = form.save(commit=False)
            request.user.bank_details = bank
            bank.save()
            request.user.save()
            return redirect(reverse('dashboard:view-profile', args=[username]))
    else:
        form = EditBankDetailsForm()

    return render(request, 'dashboard/form.html', {
        'form': form,
        'title': 'Bank Details',
    })

@login_required
def add_delivery_details(request, username):
    if request.method == 'POST':
        form = EditDeliveryDetailsForm(request.POST, request.FILES)
        if form.is_valid():
            delivery_details = form.save(commit=False)
            request.user.delivery_address = delivery_details
            delivery_details.save()
            request.user.save()
            return redirect(reverse('dashboard:view-profile', args=[username]))
    else:
        form = EditDeliveryDetailsForm()

    return render(request, 'dashboard/form.html', {
        'form': form,
        'title': 'Delivery Details',
    })

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            form.save()
            return redirect('core:login')
    else:
        form = CustomPasswordChangeForm()

    return render(request, 'dashboard/view-profile.html', {
        'form': form

    })