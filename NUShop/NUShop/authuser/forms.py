from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from authuser.models import User, Bank, DeliveryAddress

INPUT_CLASSES = 'mb-3 w-full py-2 px-6 form-account rounded-xl'

class EditIndividualForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'username', 'email', 'contact_number', 'major', 'bio',)

        widgets = {
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'username': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'email': forms.EmailInput(attrs={
                'class': INPUT_CLASSES
            }),
            'contact_number': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'major': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
            'bio': forms.Textarea(attrs={
                'class': INPUT_CLASSES
            }),
        }

class EditStudentOrganisationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'username', 'email', 'contact_number', 'bio',)

        widgets = {
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'username': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'email': forms.EmailInput(attrs={
                'class': INPUT_CLASSES
            }),
            'contact_number': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'bio': forms.Textarea(attrs={
                'class': INPUT_CLASSES
            }),
        }

class EditBankDetailsForm(forms.ModelForm):
    class Meta:
        model = Bank
        fields = ('name', 'bank_name', 'account_number', 'otp',)

        widgets = {
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'bank_name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'account_number': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'otp': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                'autocomplete': 'off'
            }),
        }
    
class EditDeliveryDetailsForm(forms.ModelForm):
    class Meta:
        model = DeliveryAddress
        fields = ('name', 'block_unitno', 'address_line1', 'address_line2', 'postcode',)

        widgets = {
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'block_unitno': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'address_line1': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'address_line2': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'postcode': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
        }

class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')