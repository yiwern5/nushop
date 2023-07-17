from django.test import TestCase
from authuser.forms import EditDeliveryDetailsForm
from checkout.forms import EditContactForm, UpdateStatusForm, AddToCartForm

class EditDeliveryDetailsFormTest(TestCase):
    def test_edit_delivery_details_form_valid(self):
        form_data = {
            'name': 'John Doe',
            'block_unitno': 'A1',
            'address_line1': '123 Street',
            'address_line2': 'Apt 456',
            'postcode': '12345'
        }
        form = EditDeliveryDetailsForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_edit_delivery_details_form_invalid(self):
        form_data = {
            'name': '',
            'block_unitno': 'A1',
            'address_line1': '',
            'address_line2': 'Apt 456',
            'postcode': ''
        }
        form = EditDeliveryDetailsForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_edit_contact_form_valid(self):
        form_data = {
            'contact_number': '1234567890'
        }
        form = EditContactForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_edit_contact_form_invalid(self):
        form_data = {
            'contact_number': ''
        }
        form = EditContactForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_update_status_form_valid(self):
        form_data = {
            'tracking_number': 'ABC123',
            'delivery_partner': 'Example Delivery'
        }
        form = UpdateStatusForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_update_status_form_invalid(self):
        form_data = {
            'tracking_number': '',
            'delivery_partner': ''
        }
        form = UpdateStatusForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_add_to_cart_form_valid(self):
        form_data = {
            'quantity': 2,
            'options': ['Option 1', 'Option 2']
        }
        form = AddToCartForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_add_to_cart_form_invalid(self):
        form_data = {
            'quantity': 0,  # Quantity less than the minimum value
            'options': ['Option 1', 'Option 2']
        }
        form = AddToCartForm(data=form_data)
        self.assertFalse(form.is_valid())
