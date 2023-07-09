from authuser.models import User
from django.db import models

from product.models import Product
from checkout.models import OrderProduct

class Chat(models.Model):
    product = models.ForeignKey(Product, related_name='chats', on_delete=models.CASCADE, null=True)
    order_product = models.ForeignKey(OrderProduct, related_name='chats', on_delete=models.CASCADE, null=True)
    members = models.ManyToManyField(User, related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-modified_at',)
    
class ChatMessage(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='created_messages', on_delete=models.CASCADE)