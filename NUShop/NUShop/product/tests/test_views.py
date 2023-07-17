from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from product.models import Category, Product, ProductImage, Variation, Subvariation, Review
from django.core.files.uploadedfile import SimpleUploadedFile
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
        self.product_image = ProductImage.objects.create(
            image='test_image.jpg',
            uploaded_by=self.user,
            product=self.product
        )
        self.variation = Variation.objects.create(
            product=self.product,
            type='Size'
        )
        self.subvariation = Subvariation.objects.create(
            variation=self.variation,
            option='Small'
        )
        self.review = Review.objects.create(
            product=self.product,
            description='Test review',
            rating='4',
            created_by=self.user
        )

        self.client.login(username='testuser', password='testpassword')

        

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

    def test_add_variation(self):
        url = reverse('add_variation', args=[self.product.pk])
        response = self.client.post(url, data={'type': 'Color'})
        self.assertEqual(response.status_code, 302)  # Redirect status code

        variation = Variation.objects.filter(product=self.product, type='Color').first()
        self.assertIsNotNone(variation)

    def test_change_variation(self):
        url = reverse('change_variation', args=[self.variation.pk, self.product.pk])
        response = self.client.post(url, data={'type': 'Material'})
        self.assertEqual(response.status_code, 302)  # Redirect status code

        self.variation.refresh_from_db()
        self.assertEqual(self.variation.type, 'Material')

    def test_delete_variation(self):
        url = reverse('delete_variation', args=[self.variation.pk, self.product.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)  # Redirect status code

        variation_exists = Variation.objects.filter(pk=self.variation.pk).exists()
        self.assertFalse(variation_exists)

    def test_add_subvariation(self):
        url = reverse('add_subvariation', args=[self.product.pk, self.variation.pk])
        response = self.client.post(url, data={'option': 'Large'})
        self.assertEqual(response.status_code, 302)  # Redirect status code

        subvariation = Subvariation.objects.filter(variation=self.variation, option='Large').first()
        self.assertIsNotNone(subvariation)

    def test_change_subvariation(self):
        url = reverse('change_subvariation', args=[self.subvariation.pk, self.product.pk])
        response = self.client.post(url, data={'option': 'Medium'})
        self.assertEqual(response.status_code, 302)  # Redirect status code

        self.subvariation.refresh_from_db()
        self.assertEqual(self.subvariation.option, 'Medium')

    def test_delete_subvariation(self):
        url = reverse('delete_subvariation', args=[self.subvariation.pk, self.product.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)  # Redirect status code

        subvariation_exists = Subvariation.objects.filter(pk=self.subvariation.pk).exists()
        self.assertFalse(subvariation_exists)

    def test_add_review(self):
        url = reverse('add_review', args=[self.product.pk])
        response = self.client.post(url, data={'description': 'Great product', 'rating': '5'})
        self.assertEqual(response.status_code, 302)  # Redirect status code

        review = Review.objects.filter(product=self.product, description='Great product', rating='5').first()
        self.assertIsNotNone(review)

    def test_delete_review(self):
        url = reverse('delete_review', args=[self.review.pk, self.product.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)  # Redirect status code

        review_exists = Review.objects.filter(pk=self.review.pk).exists()
        self.assertFalse(review_exists)