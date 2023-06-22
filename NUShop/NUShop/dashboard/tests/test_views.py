from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.messages import get_messages
from django.test import TestCase, Client
from django.urls import reverse
from authuser.models import User
from product.models import Category, Product

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

        self.client.login(username='testuser', password='testpassword')

    def test_index(self):
        response = self.client.get(reverse('dashboard:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/index.html')

        self.assertIn('products', response.context)
        self.assertEqual(list(response.context['products']), [self.product])

        self.assertIn('user', response.context)
        self.assertEqual(response.context['user'], self.user)

    def test_mypurchases(self):
        response = self.client.get(reverse('dashboard:my-purchases'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/mypurchases.html')

    def test_mysales(self):
        response = self.client.get(reverse('dashboard:my-sales'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/mysales.html')

    def test_follow(self):
        response = self.client.post(reverse('dashboard:follow', args=['seller']))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard:view-seller', args=['seller']))

        self.user.refresh_from_db()
        self.seller.refresh_from_db()

        self.assertTrue(self.seller.followers.filter(pk=self.user.pk).exists())
        self.assertFalse(self.user.followers.filter(pk=self.seller.pk).exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You followed this seller.")

    def test_unfollow(self):
        self.seller.followers.add(self.user)
        response = self.client.post(reverse('dashboard:unfollow', args=['seller']))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard:view-seller', args=['seller']))

        self.user.refresh_from_db()
        self.seller.refresh_from_db()

        self.assertFalse(self.seller.followers.filter(pk=self.user.pk).exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You unfollowed this seller.")

    def test_view_profile(self):
        response = self.client.get(reverse('dashboard:view-profile', args=['testuser']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/view-profile.html')
        self.assertEqual(response.context['user'], self.user)