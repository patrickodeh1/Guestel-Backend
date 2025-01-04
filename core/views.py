from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, RoomForm, HotelRegistrationForm, BookingForm, HotelOwnerRegistrationForm, ReviewForm
from .models import Hotel, Room, Booking
from django.contrib import messages

USER_TYPES = {
    'user': UserRegistrationForm,
    'hotel_owner': HotelOwnerRegistrationForm,
}

def select_user_type(request):
    """
    Step 1: User selects their type.
    """
    return render(request, 'registration/select_user_type.html')


def register(request):
    user_type = request.GET.get('user_type', 'user')

    if request.method == 'POST':
        if user_type == 'hotel_owner':
            form = HotelOwnerRegistrationForm(request.POST)
        elif user_type == 'user':
            form = UserRegistrationForm(request.POST)
        else:
            form = None

        if form and form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"{user_type.replace('_', ' ').capitalize()} account created successfully!")
            return redirect('home')
        else:
            messages.error(request, "Registration failed. Please check the form.")
    else:
        if user_type == 'hotel_owner':
            form = HotelOwnerRegistrationForm()
        elif user_type == 'user':
            form = UserRegistrationForm()
        else:
            form = None

    return render(
        request,
        'registration/register.html',
        {
            'form': form,
            'user_type': user_type,
        }
    )

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
def create_hotel(request):
    if request.method == 'POST':
        form = HotelRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            hotel = form.save(commit=False)
            hotel.owner = request.user
            hotel.photo = request.FILES['photo']
            hotel.save()

            return redirect('hotel_dashboard')
    else:
        form = HotelRegistrationForm()

    return render(request, 'hotels/create_hotel.html', {'form': form})

def home(request):
  hotels = Hotel.objects.all()  # Get all hotels initially

  hotel_name = request.GET.get('hotel_name')
  if hotel_name:
    hotels = hotels.filter(name__icontains=hotel_name)  # Filter by name (case-insensitive)

  return render(request, 'home.html', {'hotels': hotels})


@login_required
def hotel_dashboard(request):
    if request.user.is_hotel_owner:
        hotels = Hotel.objects.filter(owner=request.user)
        hotel_id = request.GET.get('hotel_id')  # Assuming you have the hotel ID from a form or query string
        return render(request, 'hotels/dashboard.html', {'hotels': hotels, 'hotel_id': hotel_id})
    else:
        return redirect('home')

@login_required
def hotel_detail(request, pk):
    """
    Displays details of a specific hotel.
    """
    hotel = get_object_or_404(Hotel, pk=pk) 
    reviews = hotel.review_set.all()
    return render(request, 'hotels/hotel_detail.html', {'hotel': hotel})

@login_required
def create_room(request, pk):
    """
    Handles room creation for a specific hotel.
    """
    hotel = get_object_or_404(Hotel, id=pk, owner=request.user) 
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            room = form.save(commit=False)
            room.hotel = hotel
            room.save()
            return redirect('hotel_detail', pk=pk) 
    else:
        form = RoomForm()
    return render(request, 'hotels/create_room.html', {'form': form, 'hotel': hotel})

@login_required
def edit_room(request, pk, room_id):
    """
    Handles room editing for a specific hotel.
    """
    hotel = get_object_or_404(Hotel, id=pk, owner=request.user)
    room = get_object_or_404(Room, id=room_id, hotel=hotel) 
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES, instance=room)
        if form.is_valid():
            form.save()
            return redirect('hotel_detail', pk=pk)
    else:
        form = RoomForm(instance=room)
    return render(request, 'hotels/edit_room.html', {'form': form, 'hotel': hotel})

@login_required
def delete_room(request, pk, room_id):
    """
    Handles room deletion for a specific hotel with a confirmation step.
    """
    hotel = get_object_or_404(Hotel, id=pk, owner=request.user)
    room = get_object_or_404(Room, id=room_id, hotel=hotel)

    if request.method == 'POST':
        room.delete()
        return redirect('hotel_detail', pk=pk)
    else:
        return render(request, 'hotels/delete_room.html', {'hotel': hotel, 'room': room})

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
            return render(request, 'hotels/book_room.html', {'hotel': hotel, 'room': room, 'form': form, 'success_message': 'Your room has been booked successfully!'})
    else:
        form = BookingForm(initial={'room': room})

    return render(request, 'hotels/book_room.html', {'hotel': hotel, 'room': room, 'form': form})


def owner_bookings(request, hotel_id):
    """
    Displays a list of bookings for the specified hotel owner.
    """
    hotel = get_object_or_404(Hotel, id=hotel_id, owner=request.user) 
    bookings = Booking.objects.filter(room__hotel=hotel).order_by('-check_in_date')

    return render(request, 'hotels/owner_bookings.html', {'hotel': hotel, 'bookings': bookings})


@login_required
def logout_user(request):
    """
    Logs the current user out.
    """
    logout(request)
    return redirect('home') 


@login_required
def owner_hotel_edit(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    if request.method == 'POST':
        form = HotelRegistrationForm(request.POST, request.FILES, instance=hotel)
        if form.is_valid():
            form.save()
            return redirect('hotel_detail', pk=hotel.pk)
    else:
        form = HotelRegistrationForm(instance=hotel)
    return render(request, 'hotels/edit_hotel.html', {'form': form, 'hotel': hotel})


def owner_hotel_delete(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    if request.method == 'POST':
        hotel.delete()
        return redirect('home')
    else:
        return render(request, 'hotels/confirm_delete.html', {'hotel': hotel})


@login_required
def add_review(request, pk):
    hotel = get_object_or_404(Hotel, id=pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.hotel = hotel
            review.save()
            return redirect('hotel_detail', pk=hotel.pk)  # Redirect to hotel detail page
    else:
        form = ReviewForm()

    return render(request, 'hotels/add_review.html', {'hotel': hotel, 'form': form})