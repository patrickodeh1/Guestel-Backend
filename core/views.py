from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, HotelRegistrationForm
from .models import User, Hotel

def register(request):
  """
  Handles user registration.
  """
  if request.method == 'POST':
    form = UserRegistrationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)  # Log in the newly registered user
      return redirect('home')  # Redirect to the home page after successful registration
  else:
    form = UserRegistrationForm()
  return render(request, 'registration/register.html', {'form': form})

def login_user(request):
  """
  Handles user login.
  """
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
      login(request, user)
      return redirect('home')  # Redirect to the home page after successful login
    else:
      # Handle invalid login credentials
      error_message = 'Invalid username or password.'
      return render(request, 'registration/login.html', {'error': error_message})
  else:
    return render(request, 'registration/login.html')

@login_required
def create_hotel_profile(request):
  """
  Handles hotel profile creation for authenticated hotel owners.
  """
  if request.method == 'POST':
    form = HotelRegistrationForm(request.POST, request.FILES)  # Handle file uploads
    if form.is_valid():
      hotel = form.save(commit=False)  # Don't save yet, associate with user
      hotel.owner = request.user  # Set the current user as the hotel owner
      hotel.save()
      return redirect('home')  # Redirect to the home page after successful creation
  else:
    form = HotelRegistrationForm()
  return render(request, 'hotels/create_profile.html', {'form': form})

def home(request):
  """
  Displays the home page.
  """
  # Consider adding logic to display featured hotels or a search bar here
  return render(request, 'home.html')