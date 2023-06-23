from django.test import TestCase
from core.forms import LoginForm, SignupForm
from authuser.models import User

class TestForms(TestCase):
    def test_login_form_valid_data(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='password')

        form_data = {
            'username': 'testuser',
            'password': 'password',
        }

        form = LoginForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_login_form_invalid_data(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='password')

        form_data = {
            'username': 'testuser',
            'password': 'wrongpassword',
        }

        form = LoginForm(data=form_data)

        self.assertFalse(form.is_valid())

    def test_signup_form_valid_data(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'veryStrongPassword',
            'password2': 'veryStrongPassword',
        }

        form = SignupForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_signup_form_invalid_data(self):
        form_data = {}

        form = SignupForm(data=form_data)

        self.assertFalse(form.is_valid())