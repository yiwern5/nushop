from django.test import TestCase
from django.utils import timezone
from authuser.models import User
from product.models import Product, Category
from checkout.models import Cart, CartProduct, BuyerStatus, SellerStatus, OrderProduct
from django.core.files.uploadedfile import SimpleUploadedFile


class CartProductModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.category = Category.objects.create(name='Test Category')
        image_data = b'\x00\x01\x02\x03'  # Example image data
        self.thumbnail_file = SimpleUploadedFile('test_image.jpg', image_data, content_type='image/jpeg')
        self.product = Product.objects.create(
            category=self.category,
            name='Test Product', 
            price=20,
            is_sold=False, 
            created_by=self.user,
            thumbnail=self.thumbnail_file,
        )
        self.cart_product = CartProduct.objects.create(
            created_by=self.user,
            product=self.product,
            quantity=2
        )

    def test_cart_product_subtotal(self):
        expected_subtotal = 40

        self.assertEqual(self.cart_product.subtotal, expected_subtotal)

    def test_cart_product_string_representation(self):
        expected_string = '2 of Test Product'

        self.assertEqual(str(self.cart_product), expected_string)


class CartModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.cart = Cart.objects.create(
            created_by=self.user,
            created_at=timezone.now(),
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
            created_by=self.user,
            product=self.product,
            quantity=2
        )
        self.cart.products.add(self.cart_product)

    def test_cart_model(self):
        cart = self.cart
        expected_total_price = 40
        expected_total_quantity = 2
        expected_cart_str = f"Cart of {self.user.username}"

        self.assertEqual(cart.total_price, expected_total_price)
        self.assertEqual(cart.get_total_amount(), expected_total_price)
        self.assertEqual(cart.get_total_quantity(), expected_total_quantity)
        self.assertEqual(str(cart), expected_cart_str)

class OrderProductModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.category = Category.objects.create(name='Test Category')
        image_data = b'\x00\x01\x02\x03'  # Example image data
        self.thumbnail_file = SimpleUploadedFile('test_image.jpg', image_data, content_type='image/jpeg')
        self.product = Product.objects.create(
            category=self.category,
            name='Test Product',
            price=20,
            is_sold=False,
            created_by=self.user,
            thumbnail=self.thumbnail_file,
        )
        self.cart_product = CartProduct.objects.create(
            created_by=self.user,
            product=self.product,
            quantity=2
        )
        self.buyer_status = BuyerStatus.objects.create(name='Buyer Status')
        self.seller_status = SellerStatus.objects.create(name='Seller Status')

    def test_order_product_model(self):
        order_product = OrderProduct.objects.create(
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
        expected_string = f"Order of {self.user.username}"

        self.assertEqual(order_product.name, 'Test Order Product')
        self.assertEqual(order_product.price, 20)
        self.assertEqual(order_product.thumbnail, self.thumbnail_file)
        self.assertEqual(order_product.quantity, 2)
        self.assertEqual(str(order_product), expected_string)