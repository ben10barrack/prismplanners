from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from .models import Guest, Venue, Transport, Entertainment, Catering


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