from django.urls import reverse, resolve
from django.test import SimpleTestCase
from . import views
from checkout.views import CreateStripeCheckoutSessionView, SuccessView, CancelView

class TestUrls(SimpleTestCase):
    def test_index_url_resolves(self):
        url = reverse('index')
        self.assertEqual(resolve(url).func, views.index)

    def test_add_to_cart_url_resolves(self):
        url = reverse('add_to_cart', args=[1])  
        self.assertEqual(resolve(url).func, views.add_to_cart)

    def test_remove_from_cart_url_resolves(self):
        url = reverse('remove_from_cart', args=[1])  
        self.assertEqual(resolve(url).func, views.remove_from_cart)

    def test_select_cart_product_url_resolves(self):
        url = reverse('select_cart_product', args=[1])  
        self.assertEqual(resolve(url).func, views.select_cart_product)

    def test_checkout_url_resolves(self):
        url = reverse('checkout')
        self.assertEqual(resolve(url).func, views.checkout)

    def test_add_shipping_details_url_resolves(self):
        url = reverse('add_shipping_details')
        self.assertEqual(resolve(url).func, views.add_shipping_details)

    def test_edit_shipping_details_url_resolves(self):
        url = reverse('edit_shipping_details')
        self.assertEqual(resolve(url).func, views.edit_shipping_details)

    def test_create_checkout_session_url_resolves(self):
        url = reverse('create_checkout_session', args=[1])  
        self.assertEqual(resolve(url).func.view_class, CreateStripeCheckoutSessionView)

    def test_success_url_resolves(self):
        url = reverse('success')
        self.assertEqual(resolve(url).func.view_class, SuccessView)

    def test_cancel_url_resolves(self):
        url = reverse('cancel')
        self.assertEqual(resolve(url).func.view_class, CancelView)

    def test_order_details_url_resolves(self):
        url = reverse('order-details', args=[1]) 
        self.assertEqual(resolve(url).func, views.order_details)

    def test_cancel_order_url_resolves(self):
        url = reverse('cancel-order', args=[1])  
        self.assertEqual(resolve(url).func, views.cancel_order)

    def test_order_received_url_resolves(self):
        url = reverse('order-received', args=[1])  
        self.assertEqual(resolve(url).func, views.order_received)

    def test_return_refund_url_resolves(self):
        url = reverse('return-refund', args=[1])  
        self.assertEqual(resolve(url).func, views.return_refund)

    def test_update_status_url_resolves(self):
        url = reverse('update-status', args=[1])  
        self.assertEqual(resolve(url).func, views.update_status)

    def test_delivered_url_resolves(self):
        url = reverse('delivered', args=[1]) 
        self.assertEqual(resolve(url).func, views.delivered)

    def test_stripe_webhook_url_resolves(self):
        url = reverse('stripe_webhook')
        self.assertEqual(resolve(url).func, views.stripe_webhook)

    def test_decrease_from_cart_url_resolves(self):
        url = reverse('decrease_from_cart', args=[1])
        self.assertEqual(resolve(url).func, views.decrease_from_cart)

    def test_increase_from_cart_url_resolves(self):
        url = reverse('increase_from_cart', args=[1])  
        self.assertEqual(resolve(url).func, views.increase_from_cart)
