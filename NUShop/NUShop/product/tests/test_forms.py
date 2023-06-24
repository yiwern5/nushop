from django.test import TestCase
from product.forms import NewProductForm, EditProductForm, ChangeImageForm, AddImageForm
from product.models import Category
from django.core.files.uploadedfile import SimpleUploadedFile
from authuser.models import User
from product.models import Product, ProductImage

class NewProductFormTest(TestCase):
    def test_new_product_form_valid(self):
        self.category = Category.objects.create(name='Test Category')
        image_data = b'\x00\x01\x02\x03'  
        self.thumbnail_file = SimpleUploadedFile('test_image.jpg', image_data, content_type='image/jpeg')
        form_data = {
            'category': self.category,
            'name': 'Test Product',
            'description': 'This is a test product',
            'price': '20.00',
            'thumbnail': self.thumbnail_file,
        }
        form = NewProductForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_new_product_form_invalid(self):
        form_data = {
            'category': '',
            'name': 'Test Product',
            'description': '',
            'price': '',
            'thumbnail': ''
        }
        form = NewProductForm(data=form_data)
        self.assertFalse(form.is_valid())

class EditProductFormTest(TestCase):
    def test_edit_product_form_valid(self):
        form_data = {
            'name': 'Updated Product',
            'description': 'Updated description',
            'price': '25.00',
            'thumbnail': 'updated_image.jpg',
            'is_sold': True
        }
        form = EditProductForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_edit_product_form_invalid(self):
        form_data = {
            'name': '',
            'description': '',
            'price': '',
            'thumbnail': '',
            'is_sold': True
        }
        form = EditProductForm(data=form_data)
        self.assertFalse(form.is_valid())

class ChangeImageFormTest(TestCase):
    def test_change_image_form_valid(self):
        user = User.objects.create_user(
            username='testuser',
            email='nushop@gmail.com',
            password='testpassword',
        )
        category = Category.objects.create(name='Test Category')
        image_data = b'\x00\x01\x02\x03'  # Example image data
        thumbnail_file = SimpleUploadedFile('test_image.jpg', image_data, content_type='image/jpeg')
        product = Product.objects.create(
            category=category,
            name='Test Product', 
            price='20',
            is_sold=False, 
            created_by=user,
            thumbnail=thumbnail_file,
        )
        image_file = SimpleUploadedFile('test_image.jpg', image_data, content_type='image/jpeg')
        image = ProductImage.objects.create(product=product, image=image_file, uploaded_by=user)

        form_data = {
            'image': 'updated_image.jpg',
        }
        form = ChangeImageForm(data=form_data, instance=image)
        self.assertTrue(form.is_valid())

    def test_change_image_form_invalid(self):
        form_data = {
            'image': ''
        }
        form = ChangeImageForm(data=form_data)
        self.assertFalse(form.is_valid())

class AddImageFormTest(TestCase):
    def test_add_image_form_valid(self):
        user = User.objects.create_user(
            username='testuser',
            email='nushop@gmail.com',
            password='testpassword',
        )
        category = Category.objects.create(name='Test Category')
        image_data = b'\x00\x01\x02\x03'  # Example image data
        thumbnail_file = SimpleUploadedFile('test_image.jpg', image_data, content_type='image/jpeg')
        product = Product.objects.create(
            category=category,
            name='Test Product', 
            price='20',
            is_sold=False, 
            created_by=user,
            thumbnail=thumbnail_file,
        )
        image_file = SimpleUploadedFile('test_image.jpg', image_data, content_type='image/jpeg')
        image = ProductImage.objects.create(product=product, image=image_file, uploaded_by=user)

        form_data = {
            'image': 'updated_image.jpg',
        }
        form = AddImageForm(data=form_data, instance=image)
        self.assertTrue(form.is_valid())

    def test_add_image_form_invalid(self):
        form_data = {
            'image': ''
        }
        form = AddImageForm(data=form_data)
        self.assertFalse(form.is_valid())