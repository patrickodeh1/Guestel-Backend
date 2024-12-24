from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, EstablishmentRegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser


def home(request):
    return render(request, 'base.html')

def choose_registration(request):
    return render(request, 'choose_registration.html')

def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
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
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('user_login')


def verify_email(request, token):
    try:
        user = CustomUser.objects.get(profile__verification_token=token)
        user.verified = True
        user.profile.verification_token = None  # Clear the token after verification
        user.save()
        messages.success(request, "Your email has been verified!")
        return redirect('login')
    except CustomUser.DoesNotExist:
        messages.error(request, "Invalid or expired verification link.")
        return redirect('login')
