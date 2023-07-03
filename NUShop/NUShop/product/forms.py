from django import forms
from .models import Product,  ProductImage, Variation, Subvariation
from django.forms import inlineformset_factory

INPUT_CLASSES = 'mb-3 w-full py-2 px-6 form-account rounded-xl'

class NewProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category', 'name', 'description', 'price', 'thumbnail',)

        widgets = {
            'category': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'description': forms.Textarea(attrs={
                'class': INPUT_CLASSES
            }),
            'price': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'thumbnail': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            }),
        }

class EditProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'thumbnail', 'is_sold')

        widgets = {
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'description': forms.Textarea(attrs={
                'class': INPUT_CLASSES
            }),
            'price': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'thumbnail': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            }),
        }

class ChangeImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ('image',)

        widgets = {
            'image': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            }),
        }

class AddImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ('image',)

        widgets = {
            'image': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            }),
        }

class AddVariationForm(forms.ModelForm):
    class Meta:
        model = Variation
        fields = ('type',)

        widgets = {
            'type': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
        }

class AddSubvariationForm(forms.ModelForm):
    class Meta:
        model = Subvariation
        fields = ('variation','option')

        widgets = {
            'variation': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
            'option': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
        }