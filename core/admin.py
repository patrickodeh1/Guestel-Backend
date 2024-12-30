from django.contrib import admin
from .models import Hotel, Room, Booking, CustomUser
from django.contrib.auth.admin import UserAdmin


admin.site.site_header = "Hostify Adminstration"
admin.site.site_title = "Hostify Admin Dashboard"


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'city', 'user', 'phone_number')
    search_fields = ('name', 'city', 'owner__username')
    list_filter = ('city',)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'room_number', 'price_per_night', 'capacity', 'is_available')
    search_fields = ('hotel__name', 'room_number')
    list_filter = ('is_available', 'capacity')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('customer', 'room', 'check_in_date', 'check_out_date', 'is_confirmed')
    list_filter = ('is_confirmed', 'check_in_date', 'check_out_date')
    search_fields = ('customer__username', 'room__hotel__name')


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'verified_email', 'is_staff', 'is_active')
    list_filter = ('verified_email', 'is_staff', 'is_active')
