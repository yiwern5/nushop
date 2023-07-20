from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from django.db.models import Avg

# Create your models here.
class Faculty(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Faculties'


    def __str__(self):
        return self.name
    
class Major(models.Model):
    name = models.CharField(max_length=255)
    faculty_name = models.ForeignKey(Faculty, related_name='majors', on_delete=models.CASCADE)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name
    
class Role(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class DeliveryAddress(models.Model):
    name = models.CharField(max_length=50, default='')
    block_unitno = models.CharField(max_length=255, default='')
    address_line1 = models.CharField(max_length=255, default='')
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    postcode = models.CharField(
        max_length=5,
        validators=[
            RegexValidator(r'^\d{5}$', 'Enter a valid postcode.')
        ]
    )

    def __str__(self):
        return self.postcode
    
class Bank(models.Model):
    name = models.CharField(max_length=255, default='')
    bank_name = models.CharField(max_length=255, default='')
    account_number = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.name

class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        # Create and save a new user with the given email and password
        if not email:
            raise ValueError("You have not provided a valid NUS e-mail address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        # Create and save a new superuser with the given email and password
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email, password=None, **extra_fields):
        # Create and save a new superuser with the given email and password
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(email, password, **extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, default='')
    bio = models.CharField(max_length=500, blank=True, null=True)
    contact_number = models.CharField(max_length=8, default='')
    image = models.ImageField(upload_to='user_images', blank=True, null=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)
    major = models.ForeignKey(Major, related_name='major', on_delete=models.CASCADE, blank=True, null=True)
    role = models.ForeignKey(Role, related_name='users', on_delete=models.CASCADE, blank=True, null=True)
    # role = models.ForeignKey(Role, related_name='users', on_delete=models.CASCADE, default=2)
    followers = models.ManyToManyField('self', related_name="followed_by", symmetrical=False, blank=True)
    bank_details = models.ForeignKey(Bank, related_name='bank_details', on_delete=models.CASCADE, blank=True, null=True)
    delivery_address = models.ForeignKey(DeliveryAddress, related_name='delivery_address', on_delete=models.CASCADE, blank=True, null=True)
    wallet_balance = models.FloatField(default=0)

    USERNAME_FIELD = 'username'
    
    # Specify the fields that are required when creating a user via the createsuperuser management command
    REQUIRED_FIELDS = ['email']

    # Set the custom manager for the user model
    objects = CustomUserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def get_full_name(self):
        return self.name
    
    def get_short_name(self):
        return self.username 