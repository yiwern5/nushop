from django import forms
from .models import User

INPUT_CLASSES = 'w-full py-3 px-6 rounded-xl border'

class StudentOrganisationEditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'username', 'email', 'contact_number', 'bio', 'image')

        widgets = {
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'username': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'email': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'contact_number': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'bio': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'image': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            }),
        }