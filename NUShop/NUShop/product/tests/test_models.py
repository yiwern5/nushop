from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from authuser.models import User
from product.models import Category, Product, ProductImage


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')

    def test_category_model(self):
        category = self.category
        expected_name = 'Test Category'

        self.assertEqual(category.name, expected_name)
        self.assertIsNotNone(category.pk)

    def test_category_string_representation(self):
        category = self.category
        expected_string = 'Test Category'

        self.assertEqual(str(category), expected_string)


class ProductModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            category=self.category,
            name='Test Product',
            description='Test description',
            price='20.00',
            is_sold=False,
            created_by=self.user
        )

    def test_product_model(self):
        product = self.product
        expected_name = 'Test Product'
        expected_description = 'Test description'
        expected_price = '20.00'

        self.assertEqual(product.name, expected_name)
        self.assertEqual(product.description, expected_description)
        self.assertEqual(str(product.price), expected_price)
        self.assertFalse(product.is_sold)
        self.assertEqual(product.created_by, self.user)
        self.assertIsNotNone(product.created_at)

    def test_product_string_representation(self):
        product = self.product
        expected_string = 'Test Product'

        self.assertEqual(str(product), expected_string)


class ProductImageModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            category=self.category,
            name='Test Product',
            price='20.00',
            is_sold=False,
            created_by=self.user
        )
        image_data = b'\x00\x01\x02\x03'  # Example image data
        self.image_file = SimpleUploadedFile('test_image.jpg', image_data, content_type='image/jpeg')
        self.product_image = ProductImage.objects.create(
            product=self.product,
            image=self.image_file,
            uploaded_by=self.user
        )

    def test_product_image_model(self):
        product_image = self.product_image
        expected_product_name = 'Test Product'
        expected_uploaded_by = self.user

        self.assertEqual(product_image.product.name, expected_product_name)
        self.assertEqual(product_image.uploaded_by, expected_uploaded_by)
        self.assertIsNotNone(product_image.pk)

    def test_product_image_string_representation(self):
        product_image = self.product_image
        expected_string = 'Image of Test Product'

        self.assertEqual(str(product_image), expected_string)
