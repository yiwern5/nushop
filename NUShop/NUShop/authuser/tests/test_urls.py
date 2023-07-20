from django.test import SimpleTestCase
from django.urls import reverse, resolve
from authuser.views import edit_individual_details, edit_student_org_details, edit_bank_details, edit_delivery_details, add_bank_details, add_delivery_details, change_password, change_image

class TestUrls(SimpleTestCase):

    def test_edit_individual_url_is_resolved(self):
        url = reverse('authuser:individual-details', args=['username'])
        print(resolve(url))
        self.assertEquals(resolve(url).func, edit_individual_details)

    def test_edit_studentorg_url_is_resolved(self):
        url = reverse('authuser:student-org-details', args=['username'])
        print(resolve(url))
        self.assertEquals(resolve(url).func, edit_student_org_details)

    def test_edit_bank_details_url_is_resolved(self):
        url = reverse('authuser:edit-bank-details', args=['username'])
        print(resolve(url))
        self.assertEquals(resolve(url).func, edit_bank_details)

    def test_edit_delivery_details_url_is_resolved(self):
        url = reverse('authuser:edit-delivery-details', args=['username'])
        print(resolve(url))
        self.assertEquals(resolve(url).func, edit_delivery_details)

    def test_add_bank_details_url_is_resolved(self):
        url = reverse('authuser:add-bank-details', args=['username'])
        print(resolve(url))
        self.assertEquals(resolve(url).func, add_bank_details)

    def test_add_delivery_details_url_is_resolved(self):
        url = reverse('authuser:add-delivery-details', args=['username'])
        print(resolve(url))
        self.assertEquals(resolve(url).func, add_delivery_details)

    def test_change_password_url_is_resolved(self):
        url = reverse('authuser:change-password')
        print(resolve(url))
        self.assertEquals(resolve(url).func, change_password)

    def test_change_image_url_is_resolved(self):
        url = reverse('authuser:change-image', args=['username'])
        print(resolve(url))
        self.assertEquals(resolve(url).func, change_image)