from django.db import models
from authuser.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
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
    created_by = models.ForeignKey(User, related_name='cart', on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    products = models.ManyToManyField(CartProduct)
    start_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Cart of {self.created_by.username}"
    
class UserPayment(models.Model):
    app_user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_bool = models.BooleanField(default=False)
    stripe_checkout_id = models.CharField(max_length=500)

@receiver(post_save, sender=User)
def create_user_payment(sender, instance, created, **kwargs):
    if created:
        UserPayment.objects.create(app_user=instance)