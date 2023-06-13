from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Address(models.Model):
    user = models.ForeignKey(User, related_name='address', on_delete=models.CASCADE)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    blocknumber = models.CharField(max_length=255)
    zipcode = models.IntegerField()
    contactnumber = models.CharField(max_length=255)
    email = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return self.name

