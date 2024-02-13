from django.conf import settings
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from decimal import Decimal


class Venue(models.Model):
    AVAILABILITY_CHOICES = [
        ('A', 'Available'),
        ('N', 'Not Available'),
    ]

    venue_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    venue_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField()
    availability_status = models.CharField(max_length=1, choices=AVAILABILITY_CHOICES, default='A')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    email = models.EmailField()
    image = models.ImageField(upload_to='venue_images/', null=True, blank=True)

    def __str__(self):
        return self.venue_name


class Catering(models.Model):
    AVAILABILITY_CHOICES = [
        ('A', 'Available'),
        ('N', 'Not Available'),
    ]

    catering_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    service_name = models.CharField(max_length=255)
    cuisine_type = models.CharField(max_length=255)
    number_of_people = models.PositiveIntegerField()
    availability_status = models.CharField(max_length=1, choices=AVAILABILITY_CHOICES, default='A')
    rate_per_person = models.DecimalField(max_digits=10, decimal_places=2)
    menu = models.ImageField(upload_to='venue_images/', null=True, blank=True)
    menu2 = models.ImageField(upload_to='venue_images/', null=True, blank=True)

    def __str__(self):
        return self.service_name


class Entertainment(models.Model):
    AVAILABILITY_CHOICES = [
        ('A', 'Available'),
        ('N', 'Not Available'),
    ]
    ENTERTAINMENT_TYPES = [
        ('music', 'Music'),
        ('comedy', 'Comedy'),
        ('magic', 'Magic'),
        ('dance', 'Dance'),
        ('other', 'Other'),
    ]
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    entertainment_id = models.AutoField(primary_key=True)
    service_name = models.CharField(max_length=255, default='')
    entertainment_type = models.CharField(max_length=10, choices=ENTERTAINMENT_TYPES, default='other')
    description = models.TextField()
    contact = models.CharField(max_length=255)
    availability_status = models.CharField(max_length=1, choices=AVAILABILITY_CHOICES, default='A')
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.get_entertainment_type_display()} - {self.entertainment_id}"


class Guest(models.Model):
    guest_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    guest_name = models.CharField(max_length=255)
    guest_email = models.EmailField(unique=True)

    def __str__(self):
        return self.guest_name


class Transport(models.Model):
    AVAILABILITY_CHOICES = [
        ('A', 'Available'),
        ('N', 'Not Available'),
    ]

    transport_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    service_name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.CharField(max_length=50)
    availability_status = models.CharField(max_length=1, choices=AVAILABILITY_CHOICES, default='A')
    image = models.ImageField(upload_to='venue_images/', null=True, blank=True)

    def __str__(self):
        return self.service_name


class Wedding(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    venue = models.ForeignKey('Venue', on_delete=models.SET_NULL, null=True, blank=True)
    catering = models.ForeignKey('Catering', on_delete=models.SET_NULL, null=True, blank=True)
    transport = models.ForeignKey('Transport', on_delete=models.SET_NULL, null=True, blank=True)
    entertainment = models.ForeignKey('Entertainment', on_delete=models.SET_NULL, null=True, blank=True)
    guest_list = models.ManyToManyField('Guest', blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def calculate_final_price(self):
        final_price = 0

        if self.venue and self.venue.price:
            final_price += self.venue.price

        if self.catering and self.catering.rate_per_person:
            final_price += self.catering.rate_per_person * self.guest_list.count()

        if self.transport and self.transport.price:
            final_price += float(self.transport.price)

        if self.entertainment and self.entertainment.price:
            final_price += float(self.entertainment.price)

        return final_price

    def save(self, *args, **kwargs):
        self.total_price = self.calculate_final_price()
        super().save(*args, **kwargs)


class Booking(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('A', 'Accepted'),
        ('R', 'Rejected'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    booking_date = models.DateField()
    num_guests = models.PositiveIntegerField()
    contact_info = models.CharField(max_length=255)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')


class BookCatering(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('A', 'Accepted'),
        ('R', 'Rejected'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    catering = models.ForeignKey(Catering, on_delete=models.CASCADE)
    booking_date = models.DateField()
    num_guests = models.PositiveIntegerField()
    contact_info = models.CharField(max_length=255)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Total price column

    def calculate_total_price(self):
        return self.num_guests * self.catering.rate_per_person

    def save(self, *args, **kwargs):
        self.total_price = self.calculate_total_price()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking for {self.catering.service_name}"


class BookEntertainment(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('A', 'Accepted'),
        ('R', 'Rejected'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    entertainment = models.ForeignKey(Entertainment, on_delete=models.CASCADE)
    booking_date = models.DateField()
    duration_hours = models.PositiveIntegerField()  # Duration in hours
    contact_info = models.CharField(max_length=255)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def calculate_total_price(self):
        # Calculate total price based on duration and price per hour of the entertainment service
        return Decimal(self.duration_hours) * self.entertainment.price

    def save(self, *args, **kwargs):
        # Calculate total price before saving and convert to decimal
        self.total_price = self.calculate_total_price()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking for {self.entertainment.service_name}"
