from django.test import TestCase
from authuser.models import User
from product.models import Product, Category
from chat.models import Chat, ChatMessage
from django.core.files.uploadedfile import SimpleUploadedFile


class ChatModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')
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
        self.chat = Chat.objects.create(product=self.product)
        self.chat.members.set([self.user])

    def test_chat_model(self):
        chat = self.chat
        expected_product_name = 'Test Product'
        expected_member_count = 1

        self.assertEqual(chat.product.name, expected_product_name)
        self.assertEqual(chat.members.count(), expected_member_count)
        self.assertIsNotNone(chat.created_at)
        self.assertIsNotNone(chat.modified_at)


class ChatMessageModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')
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
        self.chat = Chat.objects.create(product=self.product)
        self.chat.members.set([self.user])
        self.chat_message = ChatMessage.objects.create(
            chat=self.chat,
            content='Test message',
            created_by=self.user
        )

    def test_chat_message_model(self):
        chat_message = self.chat_message
        expected_content = 'Test message'

        self.assertEqual(chat_message.content, expected_content)
        self.assertIsNotNone(chat_message.created_at)
        self.assertEqual(chat_message.created_by, self.user)
