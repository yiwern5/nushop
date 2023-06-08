from django.urls import path

from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('<int:pk>/select_cart_product/', views.select_cart_product, name='select_cart_product')
]