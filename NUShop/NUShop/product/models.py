from django.db import models
from authuser.models import User
from django.db.models import Avg
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
    stock = models.IntegerField(blank=True, null=True)
    sold = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    @property
    def average_rating(self):
        avg_rating = self.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
        if avg_rating is not None:
            avg_rating = round(avg_rating, 2)
            return avg_rating

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images')
    uploaded_by = models.ForeignKey(User, related_name='images', on_delete=models.CASCADE)

    def __str__(self):
        return f"Image of {self.product.name}"
    
class Variation(models.Model):
    product = models.ForeignKey(Product, related_name='variations', on_delete=models.CASCADE)
    type = models.CharField(max_length=255)
    def __str__(self):
        return self.type

class Subvariation(models.Model):
    variation = models.ForeignKey(Variation, related_name='subvariations', on_delete=models.CASCADE)
    option = models.CharField(max_length=255)
    stock = models.IntegerField(blank=True, null=True)
    def __str__(self):
        return self.option
    
class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    image1 = models.ImageField(upload_to='product_images')
    image2 = models.ImageField(upload_to='product_images', blank=True, null=True)
    image3 = models.ImageField(upload_to='product_images', blank=True, null=True)
    image4 = models.ImageField(upload_to='product_images', blank=True, null=True)
    image5 = models.ImageField(upload_to='product_images', blank=True, null=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    created_by = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
