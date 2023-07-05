from django.urls import path

from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('<int:pk>/', views.detail, name='detail'),
    path('new/<int:product_pk>/', views.new_chat, name='new'),
    path('order/<int:product_pk>/', views.order_chat, name='order'),
]