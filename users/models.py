from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import RegexValidator
from django.utils.crypto import get_random_string

class UserManager(BaseUserManager):
    def create_user(self, email, phone, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not phone:
            raise ValueError('Users must have a phone number')
        
        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, phone, password, **extra_fields)

phone_regex = RegexValidator(
    regex=r'^\+234\d{10}$',
    message="Phone number must be in the format: '+234XXXXXXXXXX' (14 digits total)."
)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    phone = models.CharField(validators=[phone_regex], max_length=14, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=64, blank=True, null=True)
    #phone_verification_token = models.CharField(max_length=6, blank=True, null=True)
    USER_TYPE_CHOICES = (
        ('guest', 'Guest'),
        ('host', 'Host'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='guest')
    is_email_verified = models.BooleanField(default=False)
    #is_phone_verified = models.BooleanField(default=False)
    is_identity_verified = models.BooleanField(default=False)
    is_property_verified = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']
    
    def __str__(self):
        return self.email

    def generate_verification_token(self):
        token = get_random_string(32)
        self.email_verification_token = token
        self.save()
        return token

    """def generate_phone_otp(self):
        otp = get_random_string(6, allowed_chars='0123456789')
        self.phone_verification_token = otp
        self.save()
        return otp"""