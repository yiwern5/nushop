from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:username>/view-seller/', views.viewseller, name='view-seller'),
    path('<str:username>/view-profile/', views.viewprofile, name='view-profile'),
    path('my-purchases/', views.mypurchases, name='my-purchases'),
    path('my-sales/', views.mypurchases, name='my-sales'),
    path('payment/', views.payment, name='payment'),
    path('<str:username>/follow/', views.follow, name='follow'),
    path('<str:username>/unfollow/', views.unfollow, name='unfollow'),
]