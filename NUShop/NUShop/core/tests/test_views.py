from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse
from authuser.models import User
from product.models import Category, Product
from core.forms import SignupForm

import json

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='nushop@gmail.com',
            password='testpassword',
        )
        self.category = Category.objects.create(name='Test Category')
        image_data = b'\x00\x01\x02\x03'  # Example image data
        self.thumbnail_file = SimpleUploadedFile('test_image.jpg', image_data, content_type='image/jpeg')
        self.product = Product.objects.create(
            category=self.category,
            name='Test Product', 
            price='20',
            is_sold=False, 
            created_by=self.user,
            thumbnail=self.thumbnail_file,
        )

    def test_index(self):
        response = self.client.get(reverse('core:index'))

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'core/index.html')

        self.assertIn('products', response.context)
        self.assertIn('categories', response.context)
        self.assertEqual(list(response.context['products']), [self.product])
        self.assertEqual(list(response.context['categories']), [self.category])

    def test_signup(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@email.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        response = self.client.post(reverse('core:signup'), data=form_data)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(User.objects.count(), 1)

        user = User.objects.first()
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.is_active)
        self.assertIsInstance(response.context['form'], SignupForm)

    def test_aboutus(self):
        response = self.client.get(reverse('core:aboutus'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/aboutus.html')

    def test_privacypolicy(self):
        response = self.client.get(reverse('core:privacypolicy'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/privacypolicy.html')

    def test_tnc(self):
        response = self.client.get(reverse('core:tnc'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/tnc.html')