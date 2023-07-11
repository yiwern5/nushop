from django.urls import path

from . import views
from .views import CreateStripeCheckoutSessionView, SuccessView, CancelView

app_name = 'checkout'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('<int:pk>/remove_from_cart/', views.remove_from_cart, name='remove_from_cart'),
    path('<int:pk>/decrease_from_cart/', views.decrease_from_cart, name='decrease_from_cart'),
    path('<int:pk>/increase_from_cart/', views.increase_from_cart, name='increase_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('add_shipping_details/', views.add_shipping_details, name='add_shipping_details'),
    path('edit_shipping_details/', views.edit_shipping_details, name='edit_shipping_details'),
    path('create_checkout_session/<int:pk>', CreateStripeCheckoutSessionView.as_view(), name='create_checkout_session'),
    path('success/', SuccessView.as_view(), name='success'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('<int:pk>/order_details/', views.order_details, name='order-details'),
    path('<int:pk>/cancel_order/', views.cancel_order, name='cancel-order'),
    path('<int:pk>/order_received/', views.order_received, name='order-received'),
    path('<int:pk>/return_refund/', views.return_refund, name='return-refund'),
    path('<int:pk>/update_status/', views.update_status, name='update-status'),
    path('<int:pk>/delivered/', views.delivered, name='delivered'),
    path('stripe_webhook/', views.stripe_webhook, name='stripe_webhook'),
]