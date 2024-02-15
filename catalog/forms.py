from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from .models import Guest, Venue, Transport, Entertainment, Catering, Booking, BookCatering, BookEntertainment, \
    BookTransport


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'group']

    def save(self, commit=True):
        user = super().save(commit=False)
        group = self.cleaned_data['group']

        if commit:
            user.save()
            user.groups.add(group)
            user.save()

        return user


class GuestForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = ['guest_name', 'guest_email']


class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ['venue_name', 'address', 'capacity', 'availability_status', 'price', 'email', 'image']


class TransportForm(forms.ModelForm):
    class Meta:
        model = Transport
        fields = ['service_name', 'description', 'price', 'image']


class EntertainmentForm(forms.ModelForm):
    class Meta:
        model = Entertainment
        fields = ['service_name',  'entertainment_type', 'description', 'contact', 'availability_status', 'price']
        widgets = {
            'availability_status': forms.Select(choices=Entertainment.AVAILABILITY_CHOICES),
        }


class CateringForm(forms.ModelForm):
    class Meta:
        model = Catering
        fields = ['service_name', 'cuisine_type', 'number_of_people', 'availability_status', 'rate_per_person', 'menu', 'menu2']


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['booking_date', 'num_guests', 'contact_info']
        
        
class BookCateringForm(forms.ModelForm):
    class Meta:
        model = BookCatering  # Use the BookCatering model
        fields = ['booking_date', 'num_guests', 'contact_info']  # Exclude catering field as it's passed in the view
        labels = {
            'booking_date': 'Booking Date',
            'num_guests': 'Number of Guests',
            'contact_info': 'Contact Information'
        }


class BookEntertainmentForm(forms.ModelForm):
    class Meta:
        model = BookEntertainment
        fields = ['booking_date', 'duration_hours', 'contact_info']
        labels = {
            'booking_date': 'Booking Date',
            'duration_hours': 'Duration (hours)',
            'contact_info': 'Contact Information',
        }


class BookTransportForm(forms.ModelForm):
    class Meta:
        model = BookTransport
        fields = ['booking_date', 'num_cars']
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date'}),
            'num_cars': forms.NumberInput(attrs={'min': 1}),
        }