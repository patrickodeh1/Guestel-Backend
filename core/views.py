from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, RoomForm, HotelRegistrationForm, BookingForm
from .models import User, Hotel, Room, Amenity

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
    Displays the home page with a list of available hotels.
    """
    hotels = Hotel.objects.all()

    # Price Range Filtering
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        hotels = hotels.filter(rooms__price__gte=min_price) 
    if max_price:
        hotels = hotels.filter(rooms__price__lte=max_price)

    # Amenities Filtering
    amenity_ids = request.GET.getlist('amenities') 
    if amenity_ids:
        hotels = hotels.filter(amenities__in=amenity_ids)

    # Star Rating Filtering (assuming you have a rating field in Hotel model)
    min_rating = request.GET.get('min_rating')
    if min_rating:
        hotels = hotels.filter(rating__gte=min_rating) 

    return render(request, 'home.html', {'hotels': hotels, 'amenities': Amenity.objects.all()})


@login_required
def hotel_dashboard(request):
    """
    Displays the hotel owner's dashboard.
    """
    hotel_owner = request.user 
    hotels = Hotel.objects.filter(owner=hotel_owner)
    return render(request, 'hotels/dashboard.html', {'hotels': hotels})

@login_required
def hotel_detail(request, hotel_id):
    """
    Displays details of a specific hotel.
    """
    hotel = get_object_or_404(Hotel, id=hotel_id, owner=request.user) 
    return render(request, 'hotels/hotel_detail.html', {'hotel': hotel})

@login_required
def create_room(request, hotel_id):
    """
    Handles room creation for a specific hotel.
    """
    hotel = get_object_or_404(Hotel, id=hotel_id, owner=request.user) 
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            room = form.save(commit=False)
            room.hotel = hotel 
            room.save()
            return redirect('hotel_detail', hotel_id=hotel_id) 
    else:
        form = RoomForm()
    return render(request, 'hotels/create_room.html', {'form': form, 'hotel': hotel})

@login_required
def edit_room(request, hotel_id, room_id):
    """
    Handles room editing for a specific hotel.
    """
    hotel = get_object_or_404(Hotel, id=hotel_id, owner=request.user)
    room = get_object_or_404(Room, id=room_id, hotel=hotel) 
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES, instance=room)
        if form.is_valid():
            form.save()
            return redirect('hotel_detail', hotel_id=hotel_id)
    else:
        form = RoomForm(instance=room)
    return render(request, 'hotels/edit_room.html', {'form': form, 'hotel': hotel})

@login_required
def delete_room(request, hotel_id, room_id):
    """
    Handles room deletion for a specific hotel.
    """
    hotel = get_object_or_404(Hotel, id=hotel_id, owner=request.user)
    room = get_object_or_404(Room, id=room_id, hotel=hotel)
    room.delete()
    return redirect('hotel_detail', hotel_id=hotel_id)

@login_required
def book_room(request, hotel_id, room_id):
    """
    Handles room booking.
    """
    hotel = get_object_or_404(Hotel, id=hotel_id)
    room = get_object_or_404(Room, id=room_id, hotel=hotel)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user 
            booking.room = room
            booking.save()
            return redirect('booking_success')  # Redirect to success page
    else:
        form = BookingForm(initial={'room': room}) 

    return render(request, 'hotels/book_room.html', {'hotel': hotel, 'room': room, 'form': form})

@login_required
def booking_success(request):
    """
    Displays a success message after a successful booking.
    """
    return render(request, 'hotels/booking_success.html')

@login_required
def logout_user(request):
    """
    Logs the current user out.
    """
    logout(request)
    return redirect('home') 