from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.messages import get_messages
from django.test import TestCase, Client
from django.urls import reverse
from authuser.models import User
from product.models import Category, Product
from checkout.models import Cart, CartProduct
from django.utils import timezone

import json

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='nushop@gmail.com',
            password='testpassword',
        )
        self.seller = User.objects.create_user(
            username='seller',
            email='seller@gmail.com',
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
        self.cart_product = CartProduct.objects.create(
             created_by = self.user,
             ordered = False,
             product = self.product,
             quantity = 1,
        )
        self.cart = Cart.objects.create(
             created_by=self.user,
             created_at=timezone.now(),
        )

        self.client.login(username='testuser', password='testpassword')

    def test_index(self):
        response = self.client.get(reverse('checkout:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout.html')
        self.assertIn('products', response.context)
        self.assertTemplateUsed('checkout/checkout.html')

    def test_add_to_cart_GET(self):
        response = self.client.get(reverse('checkout:add_to_cart', args=[1]))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed('product:detail')

    def test_add_to_cart_POST(self):
        response = self.client.post(reverse('checkout:add_to_cart', args=[1]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('product:detail', args=[1]))

        self.assertEqual(CartProduct.objects.count(), 1)
        self.assertEqual(CartProduct.objects.first().created_by, self.user)
        self.assertTemplateUsed('product:detail')

    def test_remove_from_cart_GET(self):
        self.cart.products.add(self.cart_product)

        # Make a GET request to the remove from cart URL
        response = self.client.get(reverse('checkout:remove_from_cart', args=[1]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('checkout:index'))

        self.cart.refresh_from_db()

        self.assertEqual(self.cart.products.count(), 0)
        self.assertFalse(CartProduct.objects.filter(pk=self.cart_product.pk).exists())
        self.assertTemplateUsed('checkout:index')

    def test_checkout_GET(self):
        response = self.client.get(reverse('checkout:checkout'))

        self.assertEqual(response.status_code, 200)

        self.assertIn('products', response.context)
        self.assertIn('cart', response.context)
        self.assertTemplateUsed('checkout/checkout.html')

    def test_add_shipping_details_GET(self):
        response = self.client.get(reverse('checkout:add_shipping_details', args=['testuser']))

        self.assertEqual(response.status_code, 200)

        self.assertIn('form', response.context)
        self.assertTemplateUsed('checkout:checkout')

    def test_add_shipping_details_POST(self):
        response = self.client.post(reverse('checkout:add_shipping_details', args=['testuser']))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('checkout:checkout')

    def test_edit_shipping_details_GET(self):
        response = self.client.get(reverse('checkout:edit_shipping_details', args=['testuser']))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertTemplateUsed('checkout/form.html')

    def test_edit_shipping_details_POST(self):
        response = self.client.post(reverse('checkout:edit_shipping_details', args=['testuser']))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('checkout/form.html')

