from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('select-user-type/', views.select_user_type, name='select_user_type'),
    path('login/', views.login_user, name='login'), 
    path('logout/', views.logout_user, name='logout'), 
    path('hotels/', views.hotel_dashboard, name='hotel_dashboard'), 
    path('hotels/<int:pk>/', views.hotel_detail, name='hotel_detail'),
    path('hotels/create/', views.create_hotel, name='create_hotel'),
    path('hotels/<int:pk>/create-room/', views.create_room, name='create_room'), 
    path('hotels/<int:pk>/rooms/<int:room_id>/edit/', views.edit_room, name='edit_room'), 
    path('hotels/<int:pk>/rooms/<int:room_id>/delete/', views.delete_room, name='delete_room'), 
    path('hotels/<int:hotel_id>/book-room/<int:room_id>/', views.book_room, name='book_room'), 
    path('booking-success/', views.booking_success, name='booking_success'),
    path('hotel/<int:pk>/edit/', views.owner_hotel_edit, name='owner_hotel_edit'),
    path('hotel/<int:pk>/delete/', views.owner_hotel_delete, name='owner_hotel_delete'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

