from django.contrib import admin
from .models import Cart, CartProduct, BuyerStatus, SellerStatus, OrderProduct

admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(BuyerStatus)
admin.site.register(SellerStatus)
admin.site.register(OrderProduct)