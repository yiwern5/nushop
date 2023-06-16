from django.db import models
from authuser.models import User
from product.models import Product

# Create your models here.
class CartProduct(models.Model):
    created_by = models.ForeignKey(User, related_name='cart_product', on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
 
    def __str__(self):
        return f"{self.quantity} of {self.product.name}"
    
class Cart(models.Model):
    def get_total_amount(self):
        total_amount = 0
        for cart_product in self.products.all():
            total_amount += cart_product.quantity * cart_product.product.price
        return total_amount
    
    def get_total_quantity(self):
        total_quantity = 0
        for cart_product in self.products.all():
            total_quantity += cart_product.quantity
        return total_quantity
    
    created_by = models.ForeignKey(User, related_name='cart', on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    products = models.ManyToManyField(CartProduct)
    start_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Cart of {self.created_by.username}"
    