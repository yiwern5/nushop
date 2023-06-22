from django.test import TestCase
from authuser.models import Faculty, Major, Role, DeliveryAddress, Bank, User

class TestModel(TestCase):
    def test_create_faculty(self):
        faculty = Faculty.objects.create(name='Computing')
        saved_faculty = Faculty.objects.get(name='Computing')
        self.assertEqual(saved_faculty.name, faculty.name)

    def test_create_major(self):
        faculty = Faculty.objects.create(name='Computing')
        major = Major.objects.create(name='Computer Science', faculty_name=faculty)
        saved_major = Major.objects.get(name='Computer Science')
        self.assertEqual(saved_major.name, major.name)
        self.assertEqual(saved_major.faculty_name, major.faculty_name)

    def test_create_role(self):
        role = Role.objects.create(name='Admin')
        saved_role = Role.objects.get(name='Admin')
        self.assertEqual(saved_role.name, role.name)

    def test_create_delivery_address(self):
        delivery_address = DeliveryAddress.objects.create(
            name='John Doe',
            block_unitno='A-123',
            address_line1='123 Main St',
            address_line2='Apt 456',
            postcode='12345'
        )

        saved_delivery_address = DeliveryAddress.objects.get(name='John Doe')

        self.assertEqual(saved_delivery_address.name, delivery_address.name)
        self.assertEqual(saved_delivery_address.block_unitno, delivery_address.block_unitno)
        self.assertEqual(saved_delivery_address.address_line1, delivery_address.address_line1)
        self.assertEqual(saved_delivery_address.address_line2, delivery_address.address_line2)
        self.assertEqual(saved_delivery_address.postcode, delivery_address.postcode)

    def test_create_bank(self):
        bank = Bank.objects.create(
            name='John Doe',
            bank_name='Example Bank',
            account_number='1234567890'
        )

        saved_bank = Bank.objects.get(name='John Doe')

        self.assertEqual(saved_bank.name, bank.name)
        self.assertEqual(saved_bank.bank_name, bank.bank_name)
        self.assertEqual(saved_bank.account_number, bank.account_number)

    def test_create_user(self):
        user = User.objects.create_user(
            username='testuser',
            email='nushop@gmail.com',
            password='testpassword',
        )

        saved_user = User.objects.get(username='testuser')

        self.assertEqual(saved_user.name, user.name)
        self.assertEqual(saved_user.email, user.email)
        self.assertEqual(saved_user.password, user.password)
        self.assertFalse(saved_user.is_staff)
        self.assertFalse(saved_user.is_superuser)

    def test_create_superuser(self):
        user = User.objects.create_superuser(
            username='admin',
            email='nushop@gmail.com',
            password='testpassword',
        )

        saved_user = User.objects.get(username='admin')

        self.assertEqual(saved_user.name, user.name)
        self.assertEqual(saved_user.email, user.email)
        self.assertEqual(saved_user.password, user.password)
        self.assertTrue(saved_user.is_staff)
        self.assertTrue(saved_user.is_superuser)