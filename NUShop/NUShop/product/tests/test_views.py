from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from product.models import Category, Product, ProductImage
from django.core.files.uploadedfile import SimpleUploadedFile
from product.forms import NewProductForm, EditProductForm, AddImageForm, ChangeImageForm
from authuser.models import User

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

        self.client.login(username='testuser', password='testpassword')

        self.product_image = ProductImage.objects.create(
            image='test_image.jpg',
            uploaded_by=self.user,
            product=self.product
        )

    def test_products(self):
        response = self.client.get(reverse('product:products'))
        self.assertEqual(response.status_code, 200)

    def test_detail(self):
        response = self.client.get(reverse('product:detail', args=[self.product.pk]))
        self.assertEqual(response.status_code, 200)

    def test_new_authenticated(self):
        response = self.client.get(reverse('product:new'))
        self.assertEqual(response.status_code, 200)

    def test_new_unauthenticated(self):
        response = self.client.get(reverse('product:new'))
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        response = self.client.post(reverse('product:delete', args=[1]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())

    def test_delete_image(self):
        response = self.client.post(reverse('product:delete_image', args=[1, 1]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(ProductImage.objects.filter(pk=self.product_image.pk).exists())

    def test_edit(self):
        response = self.client.get(reverse('product:edit', args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_change_image(self):
        response = self.client.get(reverse('product:change_image', args=[1, 1]))
        self.assertEqual(response.status_code, 200)

    def test_add_image(self):
        response = self.client.get(reverse('product:add_image', args=[1]))
        self.assertEqual(response.status_code, 200)
