from django.urls import path

from . import views

app_name = 'checkout'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('<int:pk>/remove_from_cart/', views.remove_from_cart, name='remove_from_cart'),
    path('<int:pk>/select_cart_product/', views.select_cart_product, name='select_cart_product'),
    path('checkout/', views.checkout, name='checkout'),
    path('<str:username>/add-shipping-details/', views.add_shipping_details, name='add-shipping-details'),
    path('<str:username>/edit-shipping-details/', views.edit_shipping_details, name='edit-shipping-details'),
]