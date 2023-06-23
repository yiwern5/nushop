from django.test import SimpleTestCase
from django.urls import reverse, resolve
from checkout.views import index, add_to_cart, remove_from_cart, select_cart_product, checkout, add_shipping_details, edit_shipping_details, CreateStripeCheckoutSessionView, SuccessView, CancelView

class TestUrls(SimpleTestCase):

    def test_index_url_resolves(self):
        url = reverse('checkout:index')
        self.assertEquals(resolve(url).func, index)

    def test_add_to_cart_url_resolves(self):
        url = reverse('checkout:add_to_cart', args=[1])
        self.assertEquals(resolve(url).func, add_to_cart)

    def test_remove_from_cart_url_resolves(self):
        url = reverse('checkout:remove_from_cart', args=[1])
        self.assertEquals(resolve(url).func, remove_from_cart)

    def test_select_cart_product_url_resolves(self):
        url = reverse('checkout:select_cart_product', args=[1])
        self.assertEquals(resolve(url).func, select_cart_product)

    def test_checkout_resolves(self):
        url = reverse('checkout:checkout')
        self.assertEquals(resolve(url).func, checkout)

    def test_add_shipping_details_resolves(self):
        url = reverse('checkout:add_shipping_details', args=['some-str'])
        self.assertEquals(resolve(url).func, add_shipping_details)

    def test_edit_shipping_details_resolves(self):
        url = reverse('checkout:edit_shipping_details', args=['some-str'])
        self.assertEquals(resolve(url).func, edit_shipping_details)

    def test_CreateStripeCheckoutSessionView_resolves(self):
        url = reverse('checkout:create_checkout_session', args=[1])
        self.assertEquals(resolve(url).func.view_class, CreateStripeCheckoutSessionView)
    
    def test_SuccessView_resolves(self):
        url = reverse('checkout:success')
        self.assertEquals(resolve(url).func.view_class, SuccessView)

    def test_CancelView_resolves(self):
        url = reverse('checkout:cancel')
        self.assertEquals(resolve(url).func.view_class, CancelView)