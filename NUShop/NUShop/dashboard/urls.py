from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:username>/view-seller/', views.viewseller, name='view-seller'),
    path('<str:username>/view-profile/', views.viewprofile, name='view-profile'),
    path('<str:username>/individual-details/', views.edit_individual_details, name='individual-details'),
    path('<str:username>/student-org-details/', views.edit_student_org_details, name='student-org-details'),
    path('<str:username>edit-bank-details/', views.edit_bank_details, name='edit-bank-details'),
    path('<str:username>/edit-delivery-details/', views.edit_delivery_details, name='edit-delivery-details'),
    path('<str:username>/add-bank-details/', views.add_bank_details, name='add-bank-details'),
    path('<str:username>/add-delivery-details/', views.add_delivery_details, name='add-delivery-details'),
    path('change-password/', views.change_password, name='change-password'),
    path('my-purchases/', views.mypurchases, name='my-purchases'),
    path('my-sales/', views.mypurchases, name='my-sales'),
    path('cart/', views.cart, name='cart'),
    path('<str:username>/follow/', views.follow, name='follow'),
    path('<str:username>/unfollow/', views.unfollow, name='unfollow'),
]