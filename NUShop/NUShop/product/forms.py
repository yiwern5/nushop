from django import forms
from .models import Product,  ProductImage
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

# class EditProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = ('name', 'description', 'price', 'image', 'is_sold')
#         widgets = {
#             'name': forms.TextInput(attrs={
#                 'class': INPUT_CLASSES
#             }),
#             'description': forms.Textarea(attrs={
#                 'class': INPUT_CLASSES
#             }),
#             'price': forms.TextInput(attrs={
#                 'class': INPUT_CLASSES
#             }),
#             'image': forms.FileInput(attrs={
#                 'class': INPUT_CLASSES
#             }),
#         }

#     def clean_price(self):
#         price = self.cleaned_data.get('price')
#         if price and price < 0:
#             raise forms.ValidationError("Price must be a positive number.")
#         return price

#     def save(self, commit=True):
#         product = super().save(commit=commit)
#         # Additional save logic if needed
#         return product

# class EditProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = ('name', 'description', 'price', 'is_sold')

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         ProductImageFormSet = inlineformset_factory(
#             Product,
#             ProductImage,
#             form=ProductImageForm,
#             extra=1,  # Number of extra image forms
#             can_delete=True
#         )
#         self.image_formset = ProductImageFormSet(
#             instance=self.instance,
#             prefix='image_formset'
#         )

#     def is_valid(self):
#         return super().is_valid() and self.image_formset.is_valid()

#     def save(self, commit=True):
#         product = super().save(commit=commit)
#         self.image_formset.instance = product
#         self.image_formset.save()
#         return product