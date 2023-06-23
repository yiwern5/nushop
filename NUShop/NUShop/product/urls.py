from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('', views.products, name='products'),
    path('new/', views.new, name='new'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/edit/', views.edit, name='edit'),
    path('<int:pk>/add_image/', views.add_image, name='add_image'),
    path('<int:image_id>/<int:product_id>/delete_image/', views.delete_image, name='delete_image'),
    path('<int:image_id>/<int:product_id>/change_image/', views.change_image, name='change_image'),
]