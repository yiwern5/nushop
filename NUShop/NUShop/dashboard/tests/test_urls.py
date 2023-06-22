from django.test import SimpleTestCase
from django.urls import reverse, resolve
from dashboard.views import index, viewseller, viewprofile, mypurchases, mysales, follow, unfollow

class TestUrls(SimpleTestCase):

    def test_index_url_is_resolved(self):
        url = reverse('dashboard:index')
        print(resolve(url))
        self.assertEquals(resolve(url).func, index)

    def test_view_seller_is_resolved(self):
        url = reverse('dashboard:view-seller', args=['username'])
        print(resolve(url))
        self.assertEquals(resolve(url).func, viewseller)

    def test_view_profile_is_resolved(self):
        url = reverse('dashboard:view-profile', args=['username'])
        print(resolve(url))
        self.assertEquals(resolve(url).func, viewprofile)

    def test_my_purchases_url_is_resolved(self):
        url = reverse('dashboard:my-purchases')
        print(resolve(url))
        self.assertEquals(resolve(url).func, mypurchases)

    def test_my_sales_url_is_resolved(self):
        url = reverse('dashboard:my-sales')
        print(resolve(url))
        self.assertEquals(resolve(url).func, mysales)

    def test_follow_url_is_resolved(self):
        url = reverse('dashboard:follow', args=['username'])
        print(resolve(url))
        self.assertEquals(resolve(url).func, follow)

    def test_unfollow_url_is_resolved(self):
        url = reverse('dashboard:unfollow', args=['username'])
        print(resolve(url))
        self.assertEquals(resolve(url).func, unfollow)