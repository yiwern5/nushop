from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('view-seller/', views.viewseller, name='view-seller'),
    path('my-purchases/', views.mypurchases, name='my-purchases'),
    path('my-sales/', views.mypurchases, name='my-sales'),
    path('cart/', views.cart, name='cart'),
    path('payment/', views.payment, name='payment'),
]