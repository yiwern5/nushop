from django.test import TestCase
from authuser.models import DeliveryAddress
from authuser.forms import EditDeliveryDetailsForm

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
