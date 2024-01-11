from django import forms
from .models import Product,  ProductImage, Variation, Review
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
        fields = ('name', 'description', 'price', 'discount_price', 'thumbnail', 'is_sold')

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
            'discount_price': forms.TextInput(attrs={
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
        fields = ('option', 'stock')

        widgets = {
            'option': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'stock': forms.NumberInput(attrs={
                'class': INPUT_CLASSES
            }),
        }

class EditVariationForm(forms.ModelForm):
    class Meta:
        model = Variation
        fields = ('option', 'stock') 

        widgets = {
            'option': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'stock': forms.NumberInput(attrs={
                'class': INPUT_CLASSES
            }),
        }

class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [
        (1, '1'),
        # (1.5, '1.5'),
        (2, '2'),
        # (2.5, '2.5'),
        (3, '3'),
        # (3.5, '3.5'),
        (4, '4'),
        # (4.5, '4.5'),
        (5, '5'),
    ]
    
    rating = forms.ChoiceField(choices=RATING_CHOICES)

    class Meta:
        model = Review
        fields = ('description', 'image1', 'image2', 'image3', 'image4', 'image5', 'rating')

        widgets = {
            'description': forms.Textarea(attrs={
                'class': INPUT_CLASSES
            }),
            'image1': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            }),
            'image2': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            }),
            'image3': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            }),
            'image4': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            }),
            'image5': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            }),
        }

