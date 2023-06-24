from django.test import TestCase
from chat.models import ChatMessage
from chat.forms import ChatMessageForm

class ChatMessageFormTest(TestCase):
    def test_chat_message_form_valid(self):
        form_data = {
            'content': 'Hello, this is a test message.'
        }
        form = ChatMessageForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_chat_message_form_invalid(self):
        form_data = {
            'content': ''
        }
        form = ChatMessageForm(data=form_data)
        self.assertFalse(form.is_valid())
