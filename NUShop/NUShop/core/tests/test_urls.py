from django.test import SimpleTestCase
from django.urls import reverse, resolve
from django.contrib.auth.views import LoginView
from core.views import index, aboutus, tnc, privacypolicy, signup
from core.forms import LoginForm

class TestUrls(SimpleTestCase):

    def test_index_url_is_resolved(self):
        url = reverse('core:index')
        print(resolve(url))
        self.assertEquals(resolve(url).func, index)

    def test_aboutus_is_resolved(self):
        url = reverse('core:aboutus')
        print(resolve(url))
        self.assertEquals(resolve(url).func, aboutus)

    def test_tnc_url_is_resolved(self):
        url = reverse('core:tnc')
        print(resolve(url))
        self.assertEquals(resolve(url).func, tnc)

    def test_privacypolicy_url_is_resolved(self):
        url = reverse('core:privacypolicy')
        print(resolve(url))
        self.assertEquals(resolve(url).func, privacypolicy)

    def test_signup_url_is_resolved(self):
        url = reverse('core:signup')
        print(resolve(url))
        self.assertEquals(resolve(url).func, signup)

    def test_login_view(self):
        url = reverse('core:login')
        print(resolve(url))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'core/login.html')

        view = response.context['view']
        self.assertEqual(view.__class__, LoginView)
        self.assertEqual(view.authentication_form, LoginForm)

    def test_logout_view(self):
        url = reverse('core:logout')
        print(resolve(url))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('core:login'))