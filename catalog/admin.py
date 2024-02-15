from django.contrib import admin

from .models import Venue, Catering, Entertainment, Guest, Wedding, Transport, Booking, BookCatering, BookEntertainment, BookTransport

admin.site.register(Venue)
admin.site.register(Entertainment)
admin.site.register(Catering)
admin.site.register(Guest)
admin.site.register(Wedding)
admin.site.register(Transport)
admin.site.register(Booking)
admin.site.register(BookCatering)
admin.site.register(BookEntertainment)
admin.site.register(BookTransport)

