from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('', views.products, name='products'),
    path('new/', views.new, name='new'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/edit/', views.edit, name='edit'),
    path('<int:pk>/addimage/', views.addimage, name='addimage'),
    path('<int:image_id>/<int:product_id>/deleteimage/', views.deleteimage, name='deleteimage'),
    path('<int:image_id>/<int:product_id>/changeimage/', views.changeimage, name='changeimage'),
]