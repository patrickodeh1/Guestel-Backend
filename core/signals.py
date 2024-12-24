# signals.py
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.crypto import get_random_string
from .models import CustomUser
from .tokens import account_activation_token

def send_verification_email(user, request):
    current_site = get_current_site(request)
    subject = "Activate your account"
    message = render_to_string('registration/account_activation_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
