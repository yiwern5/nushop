from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import CustomPasswordChangeForm, EditIndividualForm, EditStudentOrganisationForm, EditBankDetailsForm, EditDeliveryDetailsForm
from .models import User
from django.core.mail import send_mail
from django.conf import settings
import pyotp
from datetime import datetime, timedelta

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

def send_otp(request):
    totp = pyotp.TOTP(pyotp.random_base32(), interval=60)
    otp = totp.now()
    request.session['otp_secret_key'] = totp.secret
    valid_date = datetime.now() + timedelta(minutes=1)
    request.session['otp_valid_date'] = str(valid_date)

    subject = 'OTP for Bank Details Update'
    message = f'Your OTP is: {otp}'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [request.user.email])

@login_required
def edit_bank_details(request, username):
    user = User.objects.get(username=username)
    bank = user.bank_details
    
    if request.method == 'POST':
        form = EditBankDetailsForm(request.POST, request.FILES, instance=bank)
        if form.is_valid():
            otp = request.POST.get('otp')

            otp_secret_key = request.session['otp_secret_key']
            otp_valid_date = request.session['otp_valid_date']

            if otp_secret_key and otp_valid_date is not None:
                valid_until = datetime.fromisoformat(otp_valid_date)

                if valid_until > datetime.now():
                    totp = pyotp.TOTP(otp_secret_key, interval=60)
                    if totp.verify(otp):
                        form.save()
                        bank.otp = ''
                        bank.save()
                        messages.info(request, "Bank details are updated. If you wish to edit it again please wait for at least 5 minutes.")

                        del request.session['otp_secret_key']
                        del request.session['otp_valid_date']

                        return redirect(reverse('dashboard:view-profile', args=[username]))
                    else:
                        form.add_error('otp', 'Invalid OTP. Please try again.')
                else:
                    form.add_error('otp', 'OTP expired. Please try again.')
            else:
                form.add_error('otp', 'OTP was sent. Please try again in 60 seconds.')
    else:
        form = EditBankDetailsForm(instance=bank)
        send_otp(request)            

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
        form = EditBankDetailsForm(request.POST, request.FILES, instance=bank)
        if form.is_valid():
            otp = request.POST.get('otp')

            otp_secret_key = request.session['otp_secret_key']
            otp_valid_date = request.session['otp_valid_date']

            if otp_secret_key and otp_valid_date is not None:
                valid_until = datetime.fromisoformat(otp_valid_date)

                if valid_until > datetime.now():
                    totp = pyotp.TOTP(otp_secret_key, interval=60)
                    if totp.verify(otp):
                        bank = form.save(commit=False)
                        request.user.bank_details = bank
                        request.user.save()
            
                        bank.otp = ''
                        bank.save()
                        messages.info(request, "Bank details are added. If you wish to change it please wait for at least 5 minutes.")

                        del request.session['otp_secret_key']
                        del request.session['otp_valid_date']

                        return redirect(reverse('dashboard:view-profile', args=[username]))
                    else:
                        form.add_error('otp', 'Invalid OTP. Please try again.')
                else:
                    form.add_error('otp', 'OTP expired. Please try again.')
            else:
                form.add_error('otp', 'OTP was sent. Please try again in 60 seconds.')
    else:
        form = EditBankDetailsForm()
        send_otp(request)

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