from django.test import SimpleTestCase
from django.urls import reverse, resolve
from chat.views import new_chat, inbox, detail

class TestUrls(SimpleTestCase):

    def test_inbox_url_resolves(self):
        url = reverse('chat:inbox')
        self.assertEquals(resolve(url).func, inbox)

    def test_detail_url_resolves(self):
        url = reverse('chat:detail', args=[1])
        self.assertEquals(resolve(url).func, detail)

    def test_new_url_resolves(self):
        url = reverse('chat:new', args=[1])
        self.assertEquals(resolve(url).func, new_chat)