from django.contrib import admin
from .models import Faculty, Major, DeliveryAddress, Bank, Role, User

# Register your models here.
admin.site.register(Faculty)
admin.site.register(Major)
admin.site.register(DeliveryAddress)
admin.site.register(Bank)
admin.site.register(Role)
admin.site.register(User)