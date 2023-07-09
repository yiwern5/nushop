from django import forms
from authuser.models import DeliveryAddress



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
                'class': INPUT_CLASSES
            }),
            'postcode': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
           
        }
    
class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)
    options = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, required=False)
