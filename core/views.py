from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from .forms import UserRegistrationForm, EstablishmentRegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token
from django.conf import settings
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


def home(request):
    return render(request, 'base.html')

def choose_registration(request):
    return render(request, 'choose_registration.html')

def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            """user.is_active = False  # Deactivate the account until email verification
            user.save()"""
            login(request, user)
            return redirect('home')

            # Send email verification
            """current_site = get_current_site(request)
            subject = 'Activate Your Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

            return HttpResponse('Please check your email to confirm your account.')"""
    else:
        form = UserRegistrationForm()
    return render(request, 'user_register.html', {'form': form})


def establishment_register(request):
    if request.method == 'POST':
        form = EstablishmentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = EstablishmentRegistrationForm()
    return render(request, 'establishment_register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_active:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Your account is not yet active. Please check your mail for activation link')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('user_login')
