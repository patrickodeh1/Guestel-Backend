from django.db import models
from django.contrib.auth.models import AbstractUser

"""
User Model: Extends AbstractUser to include is_hotel_owner field.
"""
class User(AbstractUser):
    is_hotel_owner = models.BooleanField(default=False) 
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, unique=True) 
    email = models.EmailField(unique=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',  # Add a related_name here
        blank=True,
        help_text='The groups this user belongs to. A user can belong to multiple groups.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',  # Add a related_name here
        blank=True,
        help_text='Specific permissions for this user.'
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

"""
Amenity Model: Defines available amenities for hotels.
"""
class Amenity(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

"""
Hotel Photo Model: Stores images related to a hotel.
"""
class HotelPhoto(models.Model):
    hotel = models.ForeignKey('Hotel', on_delete=models.CASCADE) 
    image = models.ImageField(upload_to='hotel_photos/') 

"""
Hotel Model: Represents a hotel with its details, photos, and owner.
"""
class Hotel(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    description = models.TextField()
    logo = models.ImageField(upload_to='hotel_logos/', blank=True) 
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_hotels')
    amenities = models.ManyToManyField(Amenity) 
    photos = models.ManyToManyField(HotelPhoto, blank=True, related_name='hotels') 
    rating = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True) 
    phone_number = models.CharField(max_length=20, unique=True) 
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

"""
Room Image Model: Stores images for individual rooms.
"""
class RoomImage(models.Model):
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='room_photos/')

"""
Room Model: Represents a room within a hotel.
"""
class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    room_type = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    availability = models.BooleanField(default=True) 
    description = models.TextField(blank=True)
    images = models.ManyToManyField(RoomImage, blank=True, related_name='rooms')

    def __str__(self):
        return f"{self.hotel.name} - {self.room_type}"

"""
Booking Model: Represents a hotel booking.
"""
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    number_of_guests = models.IntegerField()
    status = models.CharField(max_length=20, default='Pending') 

"""
Review Model: Allows users to leave reviews for hotels.
"""
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)]) 
    comment = models.TextField(blank=True)
