from django.test import TestCase, Client
from django.urls import reverse
from authuser.models import User
from authuser.forms import EditIndividualForm, EditStudentOrganisationForm, EditBankDetailsForm, EditDeliveryDetailsForm
from django.contrib.messages import get_messages

import json

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='nushop@gmail.com',
            password='testpassword',
        )
        self.client.login(username='testuser', password='testpassword')

    def test_edit_individual_details(self):
        data = {
            'name': 'testname',
            'username': 'testusername',
            'email': 'test@gmail.com',
            'contact_number': '12345678',
            'bio' : 'testbio',
        }

        response = self.client.post(reverse('authuser:individual-details', args=['testuser']), data)

        self.assertEqual(response.status_code, 302)

        self.assertEqual(response.url, reverse('dashboard:view-profile', args=['testuser']))

        updated_user = User.objects.get(username='testusername')
        self.assertEqual(updated_user.name, 'testname')
        self.assertEqual(updated_user.username, 'testusername')
        self.assertEqual(updated_user.email, 'test@gmail.com')
        self.assertEqual(updated_user.contact_number, '12345678')
        self.assertEqual(updated_user.bio, 'testbio')

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Personal details are updated.")

    def test_edit_individual_details_GET(self):
        response = self.client.get(reverse('authuser:individual-details', args=['testuser']))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], EditIndividualForm)
        self.assertTemplateUsed(response, 'authuser/form.html')

    def test_edit_student_org_details(self):
        data = {
            'name': 'testname',
            'username': 'testusername',
            'email': 'test@gmail.com',
            'contact_number': '12345678',
            'bio' : 'testbio',
        }

        response = self.client.post(reverse('authuser:student-org-details', args=['testuser']), data)

        self.assertEqual(response.status_code, 302)

        self.assertEqual(response.url, reverse('dashboard:view-profile', args=['testuser']))

        updated_user = User.objects.get(username='testusername')
        self.assertEqual(updated_user.name, 'testname')
        self.assertEqual(updated_user.username, 'testusername')
        self.assertEqual(updated_user.email, 'test@gmail.com')
        self.assertEqual(updated_user.contact_number, '12345678')
        self.assertEqual(updated_user.bio, 'testbio')

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Personal details are updated.")

    def test_edit_studentorg_details_GET(self):
        response = self.client.get(reverse('authuser:student-org-details', args=['testuser']))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], EditStudentOrganisationForm)
        self.assertTemplateUsed(response, 'authuser/form.html')

    def test_add_bank_details(self):
        form_data = {
            'name': 'testname',
            'bank_name': 'testbankname',
            'account_number': '12345678',
        }
        response = self.client.post(reverse('authuser:add-bank-details', args=['testuser']), data=form_data)
        self.assertEqual(response.status_code, 302)

        self.user.refresh_from_db()
        self.assertIsNotNone(self.user.bank_details)
        self.assertRedirects(response, reverse('dashboard:view-profile', args=['testuser']))

    def test_edit_bank_details(self):
        form_data = {
            'name': 'testname',
            'bank_name': 'testbankname',
            'account_number': '12345678',
        }
        response = self.client.post(reverse('authuser:add-bank-details', args=['testuser']), form_data)
    
        edit_data = {
            'name': 'editname',
            'bank_name': 'editbankname',
            'account_number': '87654321',
        }

        response = self.client.post(reverse('authuser:edit-bank-details', args=['testuser']), edit_data)

        self.assertEqual(response.status_code, 302)

        self.assertEqual(response.url, reverse('dashboard:view-profile', args=['testuser']))

        updated_user = User.objects.get(username='testuser')
        self.assertEqual(updated_user.bank_details.name, 'editname')
        self.assertEqual(updated_user.bank_details.bank_name, 'editbankname')
        self.assertEqual(updated_user.bank_details.account_number, '87654321')

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 2)
        self.assertEqual(str(messages[0]), "Bank details are added.")
        self.assertEqual(str(messages[1]), "Bank details are updated.")

    def test_edit_bank_details_GET(self):
        response = self.client.get(reverse('authuser:edit-bank-details', args=['testuser']))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], EditBankDetailsForm)
        self.assertTemplateUsed(response, 'authuser/form.html')

    def test_add_delivery_details(self):
        form_data = {
            'name': 'testname',
            'block_unitno': 'testblock_unitno',
            'address_line1': 'testaddress_line1',
            'address_line2': 'testaddress_line2',
            'postcode': '12345',
        }
        response = self.client.post(reverse('authuser:add-delivery-details', args=['testuser']), data=form_data)
        self.assertEqual(response.status_code, 302)

        self.user.refresh_from_db()
        self.assertIsNotNone(self.user.delivery_address)
        self.assertRedirects(response, reverse('dashboard:view-profile', args=['testuser']))

    def test_edit_delivery_details(self):
        form_data = {
            'name': 'testname',
            'block_unitno': 'testblock_unitno',
            'address_line1': 'testaddress_line1',
            'address_line2': 'testaddress_line2',
            'postcode': '12345',
        }
        response = self.client.post(reverse('authuser:add-delivery-details', args=['testuser']), form_data)
    
        edit_data = {
            'name': 'editname',
            'block_unitno': 'editblock_unitno',
            'address_line1': 'editaddress_line1',
            'address_line2': 'editaddress_line2',
            'postcode': '54321',
        }

        response = self.client.post(reverse('authuser:edit-delivery-details', args=['testuser']), edit_data)

        self.assertEqual(response.status_code, 302)

        self.assertEqual(response.url, reverse('dashboard:view-profile', args=['testuser']))

        updated_user = User.objects.get(username='testuser')
        self.assertEqual(updated_user.delivery_address.name, 'editname')
        self.assertEqual(updated_user.delivery_address.block_unitno, 'editblock_unitno')
        self.assertEqual(updated_user.delivery_address.address_line1, 'editaddress_line1')
        self.assertEqual(updated_user.delivery_address.address_line2, 'editaddress_line2')
        self.assertEqual(updated_user.delivery_address.postcode, '54321')

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 2)
        self.assertEqual(str(messages[0]), "Delivery details are added.")
        self.assertEqual(str(messages[1]), "Delivery details are updated.")

    def test_edit_bank_details_GET(self):
        response = self.client.get(reverse('authuser:edit-delivery-details', args=['testuser']))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], EditDeliveryDetailsForm)
        self.assertTemplateUsed(response, 'authuser/form.html')

    def test_change_password(self):
        form_data = {
            'old_password': 'testpassword',
            'new_password1': 'newtestpassword',
            'new_password2': 'newtestpassword',
        }

        response = self.client.post(reverse('authuser:change-password'), data=form_data)

        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newtestpassword'))
        self.assertRedirects(response, reverse('core:login'))