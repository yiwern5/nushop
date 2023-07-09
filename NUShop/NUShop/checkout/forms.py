from django import forms
from authuser.models import User, DeliveryAddress
from .models import OrderProduct

INPUT_CLASSES = 'mb-3 w-full py-2 px-6 form-account rounded-xl'

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
                'class': INPUT_CLASSES,
            }),
            'postcode': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
           
        }

class EditContactForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('contact_number',)
        widgets = {
                'contact_number': forms.TextInput(attrs={
                    'class': INPUT_CLASSES
                }),
        }

class UpdateStatusForm(forms.ModelForm):
    class Meta:
        model = OrderProduct
        fields = ('tracking_number', 'delivery_partner',)
        widgets = {
                'tracking_number': forms.TextInput(attrs={
                    'class': INPUT_CLASSES
                }),
                'delivery_partner': forms.TextInput(attrs={
                    'class': INPUT_CLASSES
                }),
        }
    
class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)
    options = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, required=False)
