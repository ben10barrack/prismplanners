from django.contrib import admin

from .models import Venue, Catering, Entertainment, Guest, Wedding, Transport

admin.site.register(Venue)
admin.site.register(Entertainment)
admin.site.register(Catering)
admin.site.register(Guest)
admin.site.register(Wedding)
admin.site.register(Transport)

