from django.test import TestCase, Client
from .forms import (
    GuestForm, VenueForm, TransportForm, EntertainmentForm,
    CateringForm, BookingForm, BookCateringForm,
    BookEntertainmentForm, BookTransportForm
)
from .models import Venue, Catering, Entertainment, Guest, Transport, Booking, BookCatering, BookEntertainment, BookTransport
from django.urls import reverse
from django.contrib.auth.models import User


class TestForms(TestCase):
    def test_guest_form_valid_data(self):
        form = GuestForm(data={
            'guest_name': 'John Doe',
            'guest_email': 'john@example.com'
        })
        self.assertTrue(form.is_valid())

    def test_venue_form_valid_data(self):
        form = VenueForm(data={
            'venue_name': 'Example Venue',
            'address': '123 Main St',
            'capacity': 100,
            'availability_status': 'A',
            'price': 100.00,
            'email': 'venue@example.com',
        })
        self.assertTrue(form.is_valid())

    def test_transport_form_valid_data(self):
        form = TransportForm(data={
            'service_name': 'Example Transport',
            'description': 'Transport description',
            'price': 50.00,
        })
        self.assertTrue(form.is_valid())

    def test_entertainment_form_valid_data(self):
        form = EntertainmentForm(data={
            'service_name': 'Example Entertainment',
            'entertainment_type': 'music',
            'description': 'Entertainment description',
            'contact': 'entertainment@example.com',
            'availability_status': 'A',
            'price': 75.00,
        })
        self.assertTrue(form.is_valid())

    def test_catering_form_valid_data(self):
        form = CateringForm(data={
            'service_name': 'Example Catering',
            'cuisine_type': 'Italian',
            'number_of_people': 50,
            'availability_status': 'A',
            'rate_per_person': 20.00,
        })
        self.assertTrue(form.is_valid())

    def test_booking_form_valid_data(self):
        form = BookingForm(data={
            'booking_date': '2024-12-31',
            'num_guests': 50,
            'contact_info': 'booking@example.com',
        })
        self.assertTrue(form.is_valid())

    def test_book_catering_form_valid_data(self):
        form = BookCateringForm(data={
            'booking_date': '2024-12-31',
            'num_guests': 50,
            'contact_info': 'booking@example.com',
        })
        self.assertTrue(form.is_valid())

    def test_book_entertainment_form_valid_data(self):
        form = BookEntertainmentForm(data={
            'booking_date': '2024-12-31',
            'duration_hours': 3,
            'contact_info': 'booking@example.com',
        })
        self.assertTrue(form.is_valid())

    def test_book_transport_form_valid_data(self):
        form = BookTransportForm(data={
            'booking_date': '2024-12-31',
            'num_cars': 2,
        })
        self.assertTrue(form.is_valid())


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_registration_view(self):
        response = self.client.get(reverse('registration'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_guest_list_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('guest_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'guest_list.html')


class TestModels(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_venue_model(self):
        venue = Venue.objects.create(
            user_id=self.user,
            venue_name='Test Venue',
            address='123 Test Street',
            capacity=100,
            availability_status='A',
            price=1000,
            email='test@example.com'
        )
        self.assertEqual(venue.venue_name, 'Test Venue')
        self.assertEqual(venue.address, '123 Test Street')
        self.assertEqual(venue.capacity, 100)
        self.assertEqual(venue.availability_status, 'A')
        self.assertEqual(venue.price, 1000)
        self.assertEqual(venue.email, 'test@example.com')

    def test_catering_model(self):
        catering = Catering.objects.create(
            user_id=self.user,
            service_name='Test Catering',
            cuisine_type='Test Cuisine',
            number_of_people=50,
            availability_status='A',
            rate_per_person=20,
        )
        self.assertEqual(catering.service_name, 'Test Catering')
        self.assertEqual(catering.cuisine_type, 'Test Cuisine')
        self.assertEqual(catering.number_of_people, 50)
        self.assertEqual(catering.availability_status, 'A')
        self.assertEqual(catering.rate_per_person, 20)

    def test_entertainment_model(self):
        entertainment = Entertainment.objects.create(
            user_id=self.user,
            service_name='Test Entertainment',
            entertainment_type='music',
            description='Test description',
            contact='1234567890',
            availability_status='A',
            price=500,
        )
        self.assertEqual(entertainment.service_name, 'Test Entertainment')
        self.assertEqual(entertainment.entertainment_type, 'music')
        self.assertEqual(entertainment.description, 'Test description')
        self.assertEqual(entertainment.contact, '1234567890')
        self.assertEqual(entertainment.availability_status, 'A')
        self.assertEqual(entertainment.price, 500)

    def test_guest_model(self):
        guest = Guest.objects.create(
            user=self.user,
            guest_name='Test Guest',
            guest_email='guest@example.com',
        )
        self.assertEqual(guest.guest_name, 'Test Guest')
        self.assertEqual(guest.guest_email, 'guest@example.com')

    def test_transport_model(self):
        transport = Transport.objects.create(
            user_id=self.user,
            service_name='Test Transport',
            description='Test description',
            price=50,
            availability_status='A',
        )
        self.assertEqual(transport.service_name, 'Test Transport')
        self.assertEqual(transport.description, 'Test description')
        self.assertEqual(transport.price, 50)
        self.assertEqual(transport.availability_status, 'A')

    def test_booking_total_price_calculation(self):
        # Create a venue
        venue = Venue.objects.create(
            user_id=self.user,
            venue_name='Test Venue',
            address='123 Test Street',
            capacity=100,
            availability_status='A',
            price=1000,
            email='test@example.com'
        )

        # Create a booking for the venue
        booking = Booking.objects.create(
            user=self.user,
            venue=venue,
            booking_date='2024-02-01',
            num_guests=50,
            contact_info='Test Contact',
            status='P'
        )

        # Check if the total price of the booking is calculated correctly
        self.assertEqual(booking.venue.price * booking.num_guests, booking.total_price)

    def test_book_catering_total_price_calculation(self):
        # Create a catering service
        catering = Catering.objects.create(
            user_id=self.user,
            service_name='Test Catering',
            cuisine_type='Test Cuisine',
            number_of_people=50,
            availability_status='A',
            rate_per_person=20,
        )

        # Create a catering booking
        book_catering = BookCatering.objects.create(
            user=self.user,
            catering=catering,
            booking_date='2024-02-01',
            num_guests=50,
            contact_info='Test Contact',
            status='P'
        )

        # Check if the total price of the catering booking is calculated correctly
        self.assertEqual(book_catering.catering.rate_per_person * book_catering.num_guests, book_catering.total_price)