from django import forms 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from django.contrib.auth.models import User
from .models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('firstname', 'lastname', 'address1', 'address2', 'blocknumber', 'zipcode', 'contactnumber', 'email')

    firstname = forms.CharField(widget=forms.TextInput(attrs= {
        'placeholder': 'First Name',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))

    lastname = forms.CharField(widget=forms.TextInput(attrs= {
        'placeholder': 'Last Name',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))

    address1 = forms.CharField(widget=forms.TextInput(attrs= {
        'placeholder': 'Address 1',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))

    address2 = forms.CharField(widget=forms.TextInput(attrs= {
        'placeholder': 'Address 2 (Optional)',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))

    blocknumber = forms.CharField(widget=forms.TextInput(attrs= {
        'placeholder': 'Block Number',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))

    zipcode = forms.CharField(widget=forms.TextInput(attrs= {
        'placeholder': 'Zip Code',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))

    contactnumber = forms.CharField(widget=forms.TextInput(attrs= {
        'placeholder': 'Contact Number',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))

    email = forms.CharField(widget=forms.EmailInput(attrs= {
        'placeholder': 'Enter your Email address',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))