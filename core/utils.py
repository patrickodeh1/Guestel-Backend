import uuid
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

def generate_verification_token():
    return str(uuid.uuid4())

def send_verification_email(user):
    token = generate_verification_token()
    verification_link = f"{settings.SITE_URL}{reverse('verify_email', kwargs={'token': token})}"
    
    subject = "Verify your email address"
    message = f"Hi {user.username},\n\nPlease verify your email by clicking the link below:\n\n{verification_link}\n\nThank you!"
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
    
    # Store the token temporarily in the user's session or a cache (you can implement your preferred storage method)
    user.profile.verification_token = token
    user.profile.save()
