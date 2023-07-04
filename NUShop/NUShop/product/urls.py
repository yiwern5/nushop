from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('', views.products, name='products'),
    path('new/', views.new, name='new'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/edit/', views.edit, name='edit'),
    path('<int:pk>/add_variation/', views.add_variation, name='add_variation'),
    path('<int:variation_id>/<int:product_id>/change_variation/', views.change_variation, name='change_variation'),
    path('<int:variation_id>/<int:product_id>/delete_variation/', views.delete_variation, name='delete_variation'),
    path('<int:variation_id>/<int:product_id>/add_subvariation/', views.add_subvariation, name='add_subvariation'),
    path('<int:subvariation_id>/<int:product_id>/change_subvariation/', views.change_subvariation, name='change_subvariation'),
    path('<int:subvariation_id>/<int:product_id>/delete_subvariation/', views.delete_subvariation, name='delete_subvariation'),
    path('<int:pk>/<int:variation_id>/add_subvariation/', views.add_subvariation, name='add_subvariation'),
    path('<int:pk>/add_image/', views.add_image, name='add_image'),
    path('<int:image_id>/<int:product_id>/delete_image/', views.delete_image, name='delete_image'),
    path('<int:image_id>/<int:product_id>/change_image/', views.change_image, name='change_image'),
    path('<int:pk>/add_review/', views.add_review, name='add_review'),
]