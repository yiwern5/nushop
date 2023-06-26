from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse
from chat.models import Chat, ChatMessage
from django.contrib.auth import get_user_model
from authuser.models import User
from product.models import Category, Product

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='nushop@gmail.com',
            password='testpassword',
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

        self.chat = Chat.objects.create(
            product=self.product,
        )
        self.chat.members.set([self.user])

        self.chat_message = ChatMessage.objects.create(
            chat=self.chat,
            content='hi',
            created_by=self.user, 
        )

    def test_inbox_GET(self):
        response = self.client.get(reverse('chat:inbox'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('chats', response.context)

    def test_new_chat_GET(self):
        response = self.client.get(reverse('chat:new', args=[1]))
        self.assertEqual(response.status_code, 302)
        
    def test_new_chat_POST(self):
        response = self.client.post(reverse('chat:new', args=[self.product.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard:index'))  
        self.assertEqual(Chat.objects.count(), 1)
        self.assertEqual(Chat.objects.first().members.count(), 1)

    def test_detail_GET(self):
        response = self.client.get(reverse('chat:detail', args=[self.chat.pk]))

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Assert that the 'chat' and 'form' context variables are passed to the template
        self.assertIn('chat', response.context)
        self.assertIn('form', response.context)
