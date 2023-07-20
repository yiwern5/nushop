from django.test import TestCase
from authuser.forms import EditIndividualForm, EditStudentOrganisationForm, EditBankDetailsForm, EditDeliveryDetailsForm, CustomPasswordChangeForm, ChangeImageForm
from authuser.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

class TestForms(TestCase):
    def test_edit_ind_form_valid_data(self):
        form = EditIndividualForm(data = {
            'name': 'testname',
            'username': 'testusername',
            'email': 'test@gmail.com',
            'contact_number': '12345678',
            'bio' : 'testbio',
        })

        self.assertTrue(form.is_valid())

    def test_edit_ind_form_invalid_data(self):
        form = EditIndividualForm(data = {})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)

    def test_edit_student_org_form_valid_data(self):
        form = EditStudentOrganisationForm(data = {
            'name': 'testname',
            'username': 'testusername',
            'email': 'test@gmail.com',
            'contact_number': '12345678',
            'bio' : 'testbio',
        })

        self.assertTrue(form.is_valid())

    def test_edit_student_org_form_invalid_data(self):
        form = EditStudentOrganisationForm(data = {})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)

    def test_edit_bank_details_form_valid_data(self):
        form = EditBankDetailsForm(data = {
            'name': 'testname',
            'bank_name': 'bank_name',
            'account_number': '12345678',
        })

        self.assertTrue(form.is_valid())

    def test_edit_delivery_details_form_valid_data(self):
        form = EditDeliveryDetailsForm(data = {
            'name': 'testname',
            'block_unitno': 'testblock_unitno',
            'address_line1': 'testaddress_line1',
            'address_line2': 'testaddress_line2',
            'postcode': '12345',
        })

        self.assertTrue(form.is_valid())

    def test_edit_delivery_details_form_invalid_data(self):
        form = EditDeliveryDetailsForm(data = {
            'name': 'testname',
            'block_unitno': 'testblock_unitno',
            'address_line1': 'testaddress_line1',
            'address_line2': 'testaddress_line2',
            'postcode': '123456',
        })

        self.assertFalse(form.is_valid())

    def test_change_password_form_valid_data(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='password')

        form_data = {
            'old_password': 'password',
            'new_password1': 'new_password1',
            'new_password2': 'new_password1',
        }

        form = CustomPasswordChangeForm(user=user, data=form_data)
        self.assertTrue(form.is_valid())

    def test_change_password_form_invalid_data(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='password')

        form_data = {
            'old_password': 'password',
            'new_password1': 'new_password1',
            'new_password2': 'new_password2',
        }

        form = CustomPasswordChangeForm(user=user, data=form_data)
        self.assertFalse(form.is_valid())

    def test_change_image_form_valid_data(self):
        image_data = b'\x00\x01\x02\x03'  # Example image data
        self.image = SimpleUploadedFile('test_image.jpg', image_data, content_type='image/jpeg')
        form = ChangeImageForm(data = {
            'image': self.image,
        })

        self.assertTrue(form.is_valid())