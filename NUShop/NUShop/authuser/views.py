from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import CustomPasswordChangeForm, EditIndividualForm, EditStudentOrganisationForm, EditBankDetailsForm, EditDeliveryDetailsForm
from .models import User


# Create your views here.
@login_required
def edit_individual_details(request, username):
    user = User.objects.get(username=username)
    if request.method == 'POST':
        form = EditIndividualForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.info(request, "Personal details are updated.")
            return redirect(reverse('dashboard:view-profile', args=[username]))

    else:
        form = EditIndividualForm(instance=user)

    return render(request, 'authuser/form.html', {
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
            messages.info(request, "Personal details are updated.")
            return redirect(reverse('dashboard:view-profile', args=[username]))

    else:
        form = EditStudentOrganisationForm(instance=user)

    return render(request, 'authuser/form.html', {
        'form': form,
        'title': 'Edit Personal Details',
    })

@login_required
def edit_bank_details(request, username):
    user = User.objects.get(username=username)
    bank = user.bank_details
    if request.method == 'POST':
        form = EditBankDetailsForm(request.POST, request.FILES, instance=bank)
        if form.is_valid():
            form.save()
            messages.info(request, "Bank details are updated.")
            return redirect(reverse('dashboard:view-profile', args=[username]))
    else:
        form = EditBankDetailsForm(instance=bank)

    return render(request, 'authuser/form.html', {
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
            messages.info(request, "Delivery details are updated.")
            return redirect(reverse('dashboard:view-profile', args=[username]))
    else:
        form = EditDeliveryDetailsForm(instance=delivery_details)

    return render(request, 'authuser/form.html', {
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
            messages.info(request, "Bank details are added.")
            return redirect(reverse('dashboard:view-profile', args=[username]))
    else:
        form = EditBankDetailsForm()

    return render(request, 'authuser/form.html', {
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
            messages.info(request, "Delivery details are added.")
            return redirect(reverse('dashboard:view-profile', args=[username]))
    else:
        form = EditDeliveryDetailsForm()

    return render(request, 'authuser/form.html', {
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