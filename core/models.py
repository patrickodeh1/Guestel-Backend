from django.contrib.auth.models import AbstractUser, User
from django.conf import settings
from django.db import models


class Hotel(models.Model):
    """Represents an establishment."""
    name = models.CharField(max_length=255, help_text="Name of the hotel or establishment.")
    address = models.TextField(help_text="Full address of the establishment.")
    city = models.CharField(max_length=100, help_text="City where the establishment is located.")
    description = models.TextField(blank=True, null=True, help_text="Optional description of the establishment.")
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='hotel',
        help_text="The owner of this establishment."
    )
    latitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        blank=True, 
        null=True, 
        help_text="Geographical latitude of the establishment."
    )
    longitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        blank=True, 
        null=True, 
        help_text="Geographical longitude of the establishment."
    )

    def __str__(self):
        return self.name


class Room(models.Model):
    """Represents a room within an establishment."""
    hotel = models.ForeignKey(
        Hotel, 
        on_delete=models.CASCADE, 
        related_name='rooms',
        help_text="The establishment this room belongs to."
    )
    room_number = models.CharField(max_length=50, help_text="Unique identifier for the room.")
    price_per_night = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        help_text="Cost per night to book this room."
    )
    capacity = models.IntegerField(help_text="Maximum number of guests allowed in this room.")
    is_available = models.BooleanField(default=True, help_text="Indicates if the room is currently available.")

    def __str__(self):
        return f"{self.hotel.name} - Room {self.room_number}"


class Booking(models.Model):
    """Represents a booking made by a user."""
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='bookings',
        help_text="The user who made this booking."
    )
    room = models.ForeignKey(
        Room, 
        on_delete=models.CASCADE, 
        related_name='bookings',
        help_text="The room that is booked."
    )
    check_in_date = models.DateField(help_text="Start date of the booking.")
    check_out_date = models.DateField(help_text="End date of the booking.")
    total_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        help_text="Total cost of the booking."
    )
    is_confirmed = models.BooleanField(default=False, help_text="Indicates if the booking is confirmed.")

    def __str__(self):
        return f"Booking by {self.customer.username} for {self.room.hotel.name}"


class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',  # Avoiding conflict with 'Group.user_set'
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',  # Avoiding conflict with 'Permission.user_set'
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    verified = models.BooleanField(default=False)  # Email verification status
