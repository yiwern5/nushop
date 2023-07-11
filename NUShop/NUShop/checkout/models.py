from django.db import models
from authuser.models import User 
from product.models import Product, Subvariation

# Create your models here.
class CartProduct(models.Model):
    created_by = models.ForeignKey(User, related_name='cart_product', on_delete=models.CASCADE)
    variation = models.CharField(max_length=255, blank=True, null=True)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, related_name='cart_product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    @property
    def subtotal(self):
        if self.product.discount_price:
            return self.quantity * self.product.discount_price
        return self.quantity * self.product.price
    
    @property
    def pre_discount_subtotal(self):
        return self.quantity * self.product.price
 
    def __str__(self):
        return f"{self.quantity} of {self.product.name}"
    
class Cart(models.Model):    
    created_by = models.ForeignKey(User, related_name='cart', on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    products = models.ManyToManyField(CartProduct)
    start_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField()
    completed = models.BooleanField(default=False)
    
    @property
    def total_price(self):
        return sum(product.subtotal for product in self.products.filter(ordered=False))
    
    @property
    def amount_saved(self):
        return sum(product.pre_discount_subtotal for product in self.products.filter(ordered=False)) - sum(product.subtotal for product in self.products.filter(ordered=False))

    @property
    def subtotal(self):
        return sum(product.pre_discount_subtotal for product in self.products.filter(ordered=False))
    
    def get_total_amount(self):
        total_amount = 0
        for cart_product in self.products.filter(ordered=False):
            total_amount += cart_product.quantity * cart_product.product.price
        return total_amount
    
    def get_total_quantity(self):
        total_quantity = 0
        for cart_product in self.products.all():
            total_quantity += cart_product.quantity
        return total_quantity
    
    def __str__(self):
        return f"Cart of {self.created_by.username}"
    
class BuyerStatus(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('id',)
        verbose_name_plural = 'BuyerStatus'


    def __str__(self):
        return self.name
    
class SellerStatus(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('id',)
        verbose_name_plural = 'SellerStatus'


    def __str__(self):
        return self.name
    
class OrderProduct(models.Model):
    cart_product = models.ForeignKey(CartProduct, on_delete=models.SET_NULL, null=True)
    tracking_number = models.CharField(max_length=25, default='')
    delivery_partner = models.CharField(max_length=25, default='')
    buyer_status = models.ForeignKey(BuyerStatus, related_name='buyerstatus', on_delete=models.CASCADE)
    seller_status = models.ForeignKey(SellerStatus, related_name='sellerstatus', on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, related_name='buyer', on_delete=models.SET_NULL, null=True)
    seller = models.ForeignKey(User, related_name='seller', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    name = models.CharField(max_length=255)
    price = models.FloatField()
    subtotal = models.FloatField(null=True)
    saved = models.FloatField(null=True)
    thumbnail = models.ImageField(upload_to='orderproduct_images', null=False)
    quantity = models.IntegerField()
    variation = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Order of {self.buyer.username}"
    
    def save(self, *args, **kwargs):
        if not self.pk:  # If the instance is being created
            self.name = self.cart_product.product.name
            self.price = self.cart_product.subtotal
            self.subtotal = self.cart_product.pre_discount_subtotal
            self.saved = self.subtotal - self.price
            self.thumbnail = self.cart_product.product.thumbnail
            self.seller.wallet_balance += self.price
            self.seller.save()
            self.quantity = self.cart_product.quantity
            self.variation = self.cart_product.variation
        super().save(*args, **kwargs)