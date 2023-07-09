from django.contrib.auth import views as auth_views
from django.urls import path
from django.contrib.auth.forms import PasswordResetForm
from django.urls import path
from . import views
from .forms import LoginForm

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('tnc/', views.tnc, name='tnc'),
    path('privacypolicy/', views.privacypolicy, name='privacypolicy'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='core:login'), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='core/passwordreset.html'), name='password_reset'),
    path('password-reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='core/passwordresetdone.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='core/passwordresetconfirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='core/passwordresetcomplete.html'), name='password_reset_complete'),
]