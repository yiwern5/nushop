from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.messages import get_messages
from django.test import TestCase, Client
from django.urls import reverse
from authuser.models import User
from product.models import Category, Product
from checkout.models import Cart, CartProduct, OrderProduct
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
        self.order_product = OrderProduct.objects.create(
            cart_product=self.cart_product,
            tracking_number='12345',
            delivery_partner='Delivery Partner',
            buyer_status=self.buyer_status,
            seller_status=self.seller_status,
            buyer=self.user,
            seller=self.user,
            name='Test Order Product',
            price=20,
            thumbnail=self.thumbnail_file,
            quantity=2
        )

        self.client.login(username='testuser', password='testpassword')

    def test_index(self):
        response = self.client.get(reverse('checkout:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout.html')
        self.assertIn('products', response.context)
        self.assertTemplateUsed('checkout/index.html')

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

    def test_order_details_GET(self):
        url = reverse('checkout:order-details', args=[self.order_product.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/order_detail.html')

    def test_cancel_order_POST(self):
        url = reverse('checkout:cancel-order', args=[self.order_product.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('checkout:order-details', args=[self.order_product.pk]))
        self.order_product.refresh_from_db()
        self.assertEqual(self.order_product.buyer_status.name, 'Cancelled')
        self.assertEqual(self.order_product.seller_status.name, 'Cancelled')

    def test_return_refund_POST(self):
        url = reverse('checkout:return-refund', args=[self.order_product.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('checkout:order-details', args=[self.order_product.pk]))
        self.order_product.refresh_from_db()
        self.assertEqual(self.order_product.buyer_status.name, 'Return/Refund')
        self.assertEqual(self.order_product.seller_status.name, 'Return/Refund')

    def test_order_received_POST(self):
        url = reverse('checkout:order-received', args=[self.order_product.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('checkout:order-details', args=[self.order_product.pk]))
        self.order_product.refresh_from_db()
        self.assertEqual(self.order_product.buyer_status.name, 'Completed')

    def test_update_status_POST(self):
        url = reverse('checkout:update-status', args=[self.order_product.pk])
        data = {
            'tracking_number': '123456',
            'delivery_partner': 'Test Delivery',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('checkout:order-details', args=[self.order_product.pk]))
        self.order_product.refresh_from_db()
        self.assertEqual(self.order_product.buyer_status.name, 'To Receive')
        self.assertEqual(self.order_product.seller_status.name, 'Shipped')
        self.assertEqual(self.order_product.tracking_number, '123456')
        self.assertEqual(self.order_product.delivery_partner, 'Test Delivery')

    def test_delivered_POST(self):
        url = reverse('checkout:delivered', args=[self.order_product.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('checkout:order-details', args=[self.order_product.pk]))
        self.order_product.refresh_from_db()
        self.assertEqual(self.order_product.seller_status.name, 'Completed')

    def test_select_cart_product_POST(self):
        url = reverse('checkout:select-cart-product')
        data = {
            'ordered_products': [self.cart_product.pk]
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('checkout:index'))
        self.cart.refresh_from_db()
        self.cart_product.refresh_from_db()
        self.assertFalse(self.cart_product.ordered)
        self.assertTrue(self.cart.products.filter(ordered=True).exists())

    def test_decrease_from_cart_GET(self):
        url = reverse('checkout:decrease-from-cart', args=[self.product.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('checkout:index'))
        self.cart_product.refresh_from_db()
        self.assertEqual(self.cart_product.quantity, 1)

    def test_increase_from_cart_GET(self):
        url = reverse('checkout:increase-from-cart', args=[self.product.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('checkout:index'))
        self.cart_product.refresh_from_db()
        self.assertEqual(self.cart_product.quantity, 3)