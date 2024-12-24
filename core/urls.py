from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.choose_registration, name='choose_registration'),
    path('register/user/', views.user_register, name='user_register'),
    path('register/establishment/', views.establishment_register, name='establishment_register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.logout_view, name='logout_view'),
]
