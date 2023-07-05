from django.db import models
from authuser.models import User
from django import forms

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'


    def __str__(self):
        return self.name
    

    
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to='product_images', null=False)
    is_sold = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images')
    uploaded_by = models.ForeignKey(User, related_name='images', on_delete=models.CASCADE)

    def __str__(self):
        return f"Image of {self.product.name}"