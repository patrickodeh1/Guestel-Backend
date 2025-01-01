from django.contrib import admin
from .models import User, Amenity, HotelPhoto, Hotel, RoomImage, Room, Booking, Review

# Register your models here.
admin.site.register(User)
admin.site.register(Amenity)
admin.site.register(HotelPhoto)
admin.site.register(Hotel)
admin.site.register(RoomImage)
admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(Review)