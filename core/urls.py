from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'), 
    path('login/', views.login_user, name='login'), 
    path('logout/', views.logout_user, name='logout'), 

    path('hotels/', views.hotel_dashboard, name='hotel_dashboard'), 
    path('hotels/<int:hotel_id>/', views.hotel_detail, name='hotel_detail'), 
    path('hotels/<int:hotel_id>/create-room/', views.create_room, name='create_room'), 
    path('hotels/<int:hotel_id>/rooms/<int:room_id>/edit/', views.edit_room, name='edit_room'), 
    path('hotels/<int:hotel_id>/rooms/<int:room_id>/delete/', views.delete_room, name='delete_room'), 

    path('hotels/<int:hotel_id>/book-room/<int:room_id>/', views.book_room, name='book_room'), 
    path('booking-success/', views.booking_success, name='booking_success'), 
]