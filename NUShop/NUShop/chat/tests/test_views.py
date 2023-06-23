from django.test import TestCase, Client
from django.urls import reverse
from chat.models import Chat
from django.contrib.auth import get_user_model
from authuser.models import User

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_inbox_GET(self):
        # Authenticate the test user
        self.client.login(username='admin', password='nushop1234')

        # Make a GET request to the inbox URL
        response = self.client.get(reverse('chat:inbox'))
        
        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 302)

    def test_new_chat_GET(self):
        # Authenticate the test user
        self.client.login(username='admin', password='nushop1234')

        # Make a GET request to the inbox URL
        response = self.client.get(reverse('chat:new', args=[1]))
        
        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/new.html')