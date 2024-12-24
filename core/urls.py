from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.choose_registration, name='choose_registration'),
    path('register/user/', views.user_register, name='user_register'),
    path('register/establishment/', views.establishment_register, name='establishment_register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.logout_view, name='logout_view'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
