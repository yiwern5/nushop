from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('', views.products, name='products'),
    path('<int:pk>/', views.detail, name='detail'),
]