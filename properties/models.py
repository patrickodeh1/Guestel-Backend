from django.db import models
from django.conf import settings
from .States_lga import STATES


class Property(models.Model):
    PROPERTY_TYPES = (
        ("apartment", "Apartment"),
        ("house", "House"),
        ("hotel", "Hotel"),
        ("shortlet", "Shortlet"),
    )

    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='properties')
    title = models.CharField(max_length=255)
    description = models.TextField()
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPES)
    address = models.TextField()
    state = models.CharField(max_length=100, choices=STATES)
    city = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.state}, {self.city}"