from django.urls import path

from . import views

app_name = 'checkout'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('<int:pk>/remove_from_cart/', views.remove_from_cart, name='remove_from_cart'),
    path('<int:pk>/select_cart_product/', views.select_cart_product, name='select_cart_product'),
    path('payment/', views.payment, name='payment'),
    path('<str:username>/add-shipping-details/', views.add_shipping_details, name='add-shipping-details'),
    path('<str:username>/edit-shipping-details/', views.edit_shipping_details, name='edit-shipping-details'),
    path('payment_successful/', views.payment_successful, name='payment_successful'),
    path('payment_cancelled/', views.payment_cancelled, name='payment_cancelled'),
    path('stripe_webhook/', views.stripe_webhook, name='stripe_webhook'),
]