from django.contrib import admin
from .models import User, Amenity, Hotel, Room, Booking, Review
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

admin.site.site_header = "Hostify Administration"
admin.site.site_title = "Hostify Admin Portal"
admin.site.index_title = "Welcome to Hostify Administration Dashboard"

class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active')

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

admin.site.register(User)
admin.site.register(Hotel)
admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(Review)