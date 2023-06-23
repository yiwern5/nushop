from django.urls import path

from . import views
from .views import CreateStripeCheckoutSessionView, SuccessView, CancelView

app_name = 'checkout'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('<int:pk>/remove_from_cart/', views.remove_from_cart, name='remove_from_cart'),
    path('<int:pk>/select_cart_product/', views.select_cart_product, name='select_cart_product'),
    path('checkout/', views.checkout, name='checkout'),
    path('<str:username>/add_shipping_details/', views.add_shipping_details, name='add_shipping_details'),
    path('<str:username>/edit_shipping_details/', views.edit_shipping_details, name='edit_shipping_details'),
    path('create_checkout_session/<int:pk>', CreateStripeCheckoutSessionView.as_view(), name='create_checkout_session'),
    path('success/', SuccessView.as_view(), name='success'),
    path('cancel/', CancelView.as_view(), name='cancel'),
]