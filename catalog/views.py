from django.shortcuts import render
from django.shortcuts import render
from .models import Venue, Catering, Entertainment, Guest, Transport, Wedding, Booking, BookCatering, BookEntertainment
from django.db.models import Count
from django.shortcuts import render, redirect
from .forms import RegistrationForm, BookEntertainmentForm
from .forms import GuestForm
from django.shortcuts import get_object_or_404, redirect
from .forms import VenueForm
from .forms import TransportForm
from .forms import EntertainmentForm
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .forms import CateringForm
from .forms import BookingForm, BookCateringForm
from django.db.models import F, ExpressionWrapper, fields


# Create your views here.
def index(request):
    # Count instances for each model
    num_venues = Venue.objects.count()
    num_caterings = Catering.objects.count()
    num_entertainments = Entertainment.objects.count()
    num_guests = Guest.objects.count()
    num_transports = Transport.objects.count()
    num_weddings = Wedding.objects.count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    is_venue_vendor = request.user.is_authenticated and request.user.groups.filter(name='Venue_Vendor').exists()
    is_website_user = request.user.is_authenticated and request.user.groups.filter(name='Website Users').exists()
    is_transporter = request.user.is_authenticated and request.user.groups.filter(name='Car_hiring_services').exists()
    is_entertainer = request.user.is_authenticated and request.user.groups.filter(name='Entertainer').exists()
    is_caterer = request.user.is_authenticated and request.user.groups.filter(name='Caterer').exists()

    context = {
        'num_venues': num_venues,
        'num_caterings': num_caterings,
        'num_entertainments': num_entertainments,
        'num_guests': num_guests,
        'num_transports': num_transports,
        'num_weddings': num_weddings,
        'num_visits': num_visits,
        'is_venue_vendor': is_venue_vendor,
        'is_website_user': is_website_user,
        'is_transporter': is_transporter,
        'is_entertainer': is_entertainer,
        'is_caterer': is_caterer,
    }

    return render(request, 'index.html', context=context)


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to the login page after successful registration
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})


def add_guest(request):
    if request.method == 'POST':
        form = GuestForm(request.POST)
        if form.is_valid():
            guest = form.save(commit=False)
            guest.user = request.user  # Set the logged-in user as the owner
            guest.save()
            return redirect('guest_list')  # Redirect to the guest list page after successful addition
    else:
        form = GuestForm()

    return render(request, 'add_guest.html', {'form': form})


def guest_list(request):
    user_guests = Guest.objects.filter(user=request.user)

    context = {
        'user_guests': user_guests,
    }

    return render(request, 'guest_list.html', context)


def delete_guest(request, guest_id):
    guest = get_object_or_404(Guest, guest_id=guest_id)
    if request.method == 'POST':
        guest.delete()
    return redirect('guest_list')


@login_required
def create_venue(request):
    if request.method == 'POST':
        form = VenueForm(request.POST, request.FILES)
        if form.is_valid():
            venue = form.save(commit=False)
            venue.user_id = request.user
            venue.save()
            return redirect('my_venues')  # Redirect to a success page or wherever you want
    else:
        form = VenueForm()

    return render(request, 'venue_form.html', {'form': form})


def venue_list(request):
    # Filter venues with availability status as 'Available'
    venues = Venue.objects.filter(availability_status='A')
    return render(request, 'venue_list.html', {'venues': venues})


def view_venue(request, venue_id):
    # Retrieve the venue with the given ID or return a 404 error if not found
    is_website_user = request.user.is_authenticated and request.user.groups.filter(name='Website Users').exists()
    is_venue_vendor = request.user.is_authenticated and request.user.groups.filter(name='Venue_Vendor').exists()
    venue = get_object_or_404(Venue, pk=venue_id)
    context = {
        'venue': venue,
        'is_website_user': is_website_user,
        'is_venue_vendor': is_venue_vendor,
    }

    # Render the template with the venue details
    return render(request, 'view_venue.html', context=context)


@login_required()
def create_transport(request):
    if request.method == 'POST':
        form = TransportForm(request.POST, request.FILES)  # Note: request.FILES is needed for handling file uploads
        if form.is_valid():
            transport = form.save(commit=False)
            transport.user_id = request.user
            form.save()
            return redirect('my_cars')  # Redirect to a success page or wherever you want
    else:
        form = TransportForm()

    return render(request, 'create_transport.html', {'form': form})


def view_all_transports(request):
    all_transports = Transport.objects.all()
    return render(request, 'view_all_transports.html', {'all_transports': all_transports})


def view_transport(request, transport_id):
    is_transporter = request.user.is_authenticated and request.user.groups.filter(name='Car_hiring_services').exists()
    is_website_user = request.user.is_authenticated and request.user.groups.filter(name='Website Users').exists()
    transport = get_object_or_404(Transport, transport_id=transport_id)

    context = {
        'is_transporter': is_transporter,
        'is_website_user': is_website_user,
        'transport': transport,  # Include the transport object in the context
    }

    return render(request, 'view_transport.html', context=context)


def venue_home(request):
    return render(request, 'venue_home.html')


@login_required
def my_venues(request):
    user_venues = Venue.objects.filter(user_id=request.user)
    return render(request, 'my_venues.html', {'user_venues': user_venues})


@login_required
def edit_venue(request, venue_id):
    venue = get_object_or_404(Venue, venue_id=venue_id, user_id=request.user)

    if request.method == 'POST':
        form = VenueForm(request.POST, request.FILES, instance=venue)
        if form.is_valid():
            form.save()
            return redirect('view_venue', venue_id=venue_id)
    else:
        form = VenueForm(instance=venue)

    return render(request, 'edit_venue.html', {'form': form, 'venue': venue})


def delete_venue(request, venue_id):
    venue = get_object_or_404(Venue, pk=venue_id)

    if request.method == 'POST':
        venue.delete()
        return redirect('venue_list')

    return render(request, 'delete_venue_confirm.html', {'venue': venue})


@login_required()
def car_home(request):
    return render(request, 'car_home.html')


def my_cars(request):
    # Fetch transports for the logged-in user
    user_transports = Transport.objects.filter(user_id=request.user)

    context = {
        'user_transports': user_transports,
    }

    return render(request, 'my_cars.html', context=context)


@login_required()
def edit_transport(request, transport_id):
    transport = get_object_or_404(Transport, pk=transport_id)

    if request.method == 'POST':
        form = TransportForm(request.POST, request.FILES, instance=transport)
        if form.is_valid():
            form.save()
            return redirect('my_cars')
    else:
        form = TransportForm(instance=transport)

    return render(request, 'edit_transport.html', {'form': form, 'transport': transport})


def delete_transport(request, transport_id):
    transport = get_object_or_404(Transport, pk=transport_id)

    if request.method == 'POST':
        transport.delete()
        return redirect('my_cars')

    return render(request, 'delete_transport_confirm.html', {'transport': transport})


@login_required
def create_entertainment(request):
    if request.method == 'POST':
        form = EntertainmentForm(request.POST)
        if form.is_valid():
            entertainment = form.save(commit=False)
            entertainment.user_id = request.user
            entertainment.save()
            return redirect('entertainment_list')  # Redirect to a success page or wherever you want
    else:
        form = EntertainmentForm()

    return render(request, 'create_entertainment.html', {'form': form})


def entertainment_home(request):
    return render(request, 'entertainment_home.html')


@login_required
def entertainment_list(request):
    user_entertainments = Entertainment.objects.filter(user_id=request.user)

    context = {
        'user_entertainments': user_entertainments,
    }

    return render(request, 'entertainment_list.html', context=context)


@login_required
def view_entertainment(request, entertainment_id):
    # Get the entertainment service with the given ID or return a 404 error if not found
    entertainment = get_object_or_404(Entertainment, entertainment_id=entertainment_id, user_id=request.user)

    context = {
        'entertainment': entertainment,
    }

    return render(request, 'view_entertainment.html', context=context)


@login_required
def edit_entertainment(request, entertainment_id):
    entertainment = get_object_or_404(Entertainment, pk=entertainment_id)

    if request.method == 'POST':
        form = EntertainmentForm(request.POST, instance=entertainment)
        if form.is_valid():
            form.save()
            return redirect('view_entertainment', entertainment_id=entertainment_id)
    else:
        form = EntertainmentForm(instance=entertainment)

    return render(request, 'edit_entertainment.html', {'form': form, 'entertainment': entertainment})


@login_required
def delete_entertainment(request, entertainment_id):
    entertainment = get_object_or_404(Entertainment, pk=entertainment_id, user_id=request.user)

    if request.method == 'POST':
        entertainment.delete()
        return redirect('entertainment_list')

    return redirect('view_entertainment', entertainment_id=entertainment_id)


def all_entertainment_list(request):
    # Fetch all available entertainment records
    available_entertainments = Entertainment.objects.filter(availability_status='A')

    context = {
        'available_entertainments': available_entertainments,
    }

    return render(request, 'all_entertainment_list.html', context=context)


@login_required()
def catering_home(request):
    return render(request, 'catering_home.html')


def create_catering(request):
    if request.method == 'POST':
        form = CateringForm(request.POST, request.FILES)
        if form.is_valid():
            catering = form.save(commit=False)
            catering.user_id = request.user
            catering.save()
            return redirect('catering_list')  # Redirect to a success page or wherever you want
    else:
        form = CateringForm()

    return render(request, 'create_catering.html', {'form': form})


@login_required
def catering_list(request):
    # Retrieve catering records associated with the logged-in user
    user_caterings = Catering.objects.filter(user_id=request.user)

    # Render the template with the retrieved catering records
    return render(request, 'catering_list.html', {'user_caterings': user_caterings})


@login_required
def edit_catering(request, catering_id):
    # Retrieve the catering record from the database
    catering = get_object_or_404(Catering, pk=catering_id, user_id=request.user)

    if request.method == 'POST':
        # If the form is submitted with POST data, process the form
        form = CateringForm(request.POST, request.FILES, instance=catering)
        if form.is_valid():
            form.save()  # Save the form data to update the catering record
            return redirect('catering_list')  # Redirect to the catering list page after successful editing
    else:
        # If the request method is GET, create a form instance with the current catering record data
        form = CateringForm(instance=catering)

    # Render the edit catering template with the form and catering data
    return render(request, 'edit_catering.html', {'form': form, 'catering': catering})


def delete_catering(request, catering_id):
    catering = get_object_or_404(Catering, pk=catering_id)
    if request.method == 'POST':
        catering.delete()
        return redirect('catering_list')  # Redirect to catering list page after deletion
    return render(request, 'delete_catering_confirm.html', {'catering': catering})


def view_all_catering(request):
    # Filter catering records that are available
    available_caterings = Catering.objects.filter(availability_status='A')

    context = {
        'available_caterings': available_caterings,
    }

    return render(request, 'view_all_catering.html', context)


def view_catering(request, catering_id):
    catering = get_object_or_404(Catering, pk=catering_id)

    context = {
        'catering': catering,
    }

    return render(request, 'view_catering.html', context)


def entertainment_single(request, entertainment_id):
    # Get the entertainment record with the given ID or return a 404 error if not found
    entertainment = get_object_or_404(Entertainment, entertainment_id=entertainment_id)
    is_entertainer = request.user.is_authenticated and request.user.groups.filter(name='Entertainer').exists()
    is_website_user = request.user.is_authenticated and request.user.groups.filter(name='Website Users').exists()

    context = {
        'entertainment': entertainment,
        'is_entertainer': is_entertainer,
        'is_website_user': is_website_user,
    }

    return render(request, 'entertainment_single.html', context=context)


def delete_entertainment(request, entertainment_id):
    # Retrieve the entertainment record to be deleted
    entertainment = get_object_or_404(Entertainment, pk=entertainment_id)

    if request.method == 'POST':
        # Handle the HTTP POST request to delete the record
        entertainment.delete()
        # Redirect the user to an appropriate page after deletion
        return redirect('entertainment_list')  # Redirect to the entertainment list page after deletion
    else:
        # If the request method is not POST, render an error or redirect as needed
        pass


def book_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)  # Retrieve the venue object

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.venue = venue  # Assign the venue object to the booking
            booking.save()
            return redirect('booking_confirmation')  # Redirect to a confirmation page
    else:
        form = BookingForm()

    return render(request, 'book_venue.html', {'form': form, 'venue': venue})


def booking_confirmation(request):
    return render(request, 'venue_booking_confirmation.html')


def booked_venues(request):
    # Retrieve bookings associated with the logged-in user
    user_bookings = Booking.objects.filter(user=request.user)

    context = {
        'user_bookings': user_bookings,
    }

    return render(request, 'booked_venues.html', context)


def vendor_bookings(request):
    # Retrieve bookings associated with venues owned by the current vendor
    vendor_bookings = Booking.objects.filter(venue__user_id=request.user)

    context = {
        'vendor_bookings': vendor_bookings,
    }

    return render(request, 'vendor_bookings.html', context)


def change_booking_status(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        booking.status = new_status

        # If the new status is accepted, update the availability status of the venue
        if new_status == 'A':
            venue = booking.venue
            venue.availability_status = 'N'  # Update availability to 'Not Available'
            venue.save()

        booking.save()
        return redirect('vendor_bookings')

    return redirect('vendor_bookings')


def book_catering(request, catering_id):
    catering = get_object_or_404(Catering, pk=catering_id)

    if request.method == 'POST':
        form = BookCateringForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.catering = catering
            booking.save()
            return redirect('catering_booking_confirmation')
    else:
        form = BookCateringForm()

    return render(request, 'book_catering.html', {'form': form, 'catering': catering})


def catering_booking_confirmation(request):
    return render(request, 'catering_booking_confirmation.html')


def user_bookings(request):
    # Retrieve bookings associated with the logged-in user
    user_bookings = BookCatering.objects.filter(user=request.user)

    context = {
        'user_bookings': user_bookings,
    }

    return render(request, 'user_bookings.html', context)


def caterer_bookings(request):
    # Retrieve booked caterings associated with the caterer
    caterer_bookings = BookCatering.objects.filter(catering__user_id=request.user)

    context = {
        'caterer_bookings': caterer_bookings,
    }

    return render(request, 'caterer_bookings.html', context)


def update_booking_status(request, booking_id):
    booking = get_object_or_404(BookCatering, pk=booking_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status == 'A':  # Check if the new status is "Accepted"
            booking.status = new_status
            booking.catering.availability_status = 'N'  # Change availability status to "Not Available"
            booking.catering.save()  # Save the changes to the catering object
        else:
            booking.status = new_status
        booking.save()

    return redirect('caterer_bookings')


def book_entertainment(request, entertainment_id):
    entertainment = get_object_or_404(Entertainment, pk=entertainment_id)

    if request.method == 'POST':
        form = BookEntertainmentForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.entertainment = entertainment  # Assign the entertainment object to the booking
            booking.user = request.user  # Capture the ID of the booking user
            booking.save()
            return redirect('enta_booking_confirmation')  # Redirect to a confirmation page
    else:
        form = BookEntertainmentForm()

    return render(request, 'book_entertainment.html', {'form': form, 'entertainment': entertainment})


def enta_booking_confirmation(request):
    return render(request, 'enta_booking_confirmation.html')


def my_entertainment_bookings(request):
    # Retrieve the entertainment bookings associated with the logged-in user
    user_ent_bookings = BookEntertainment.objects.filter(user=request.user)

    context = {
        'user_ent_bookings': user_ent_bookings,
    }
    return render(request, 'my_ent_bookings.html', context)


from django.shortcuts import render, get_object_or_404, redirect
from .models import BookEntertainment

def entertainer_bookings(request):
    # Retrieve bookings for the current entertainer (assuming the entertainer's ID is stored in request.user)
    entertainer_bookings = BookEntertainment.objects.filter(entertainment__user_id=request.user)

    if request.method == 'POST':
        # Handle form submission to update booking status
        booking_id = request.POST.get('booking_id')
        new_status = request.POST.get('new_status')
        booking = get_object_or_404(BookEntertainment, pk=booking_id)

        # Check if status is changing to 'Accepted'
        if new_status == 'A' and booking.status != 'A':
            # Change availability status of the associated entertainment to 'Not Available'
            booking.entertainment.availability_status = 'N'
            booking.entertainment.save()

        # Update booking status
        booking.status = new_status
        booking.save()
        return redirect('entertainer_bookings')

    return render(request, 'entertainer_bookings.html', {'entertainer_bookings': entertainer_bookings})
