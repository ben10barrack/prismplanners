from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
]

urlpatterns += [
    path('register/', views.registration, name='registration'),
    path('add_guest/', views.add_guest, name='add_guest'),
    path('guest_list/', views.guest_list, name='guest_list'),
    path('delete_guest/<int:guest_id>/', views.delete_guest, name='delete_guest'),
    path('create_venue/', views.create_venue, name='create_venue'),
    path('venues/', views.venue_list, name='venue_list'),
    path('view_venue/<int:venue_id>/', views.view_venue, name='view_venue'),
    path('create_transport/', views.create_transport, name='create_transport'),
    path('view_all_transports/', views.view_all_transports, name='view_all_transports'),
    path('view_transport/<int:transport_id>/', views.view_transport, name='view_transport'),
    path('venue_home/', views.venue_home, name='venue_home'),
    path('my_venues/', views.my_venues, name='my_venues'),
    path('edit_venue/<int:venue_id>/', views.edit_venue, name='edit_venue'),
    path('delete_venue/<int:venue_id>/', views.delete_venue, name='delete_venue'),
    path('car_home/', views.car_home, name='car_home'),
    path('my_cars/', views.my_cars, name='my_cars'),
    path('edit_transport/<int:transport_id>/', views.edit_transport, name='edit_transport'),
    path('delete_transport/<int:transport_id>/', views.delete_transport, name='delete_transport'),
    path('create_entertainment/', views.create_entertainment, name='create_entertainment'),
    path('entertainment_home/', views.entertainment_home, name='entertainment_home'),
    path('entertainment_list/', views.entertainment_list, name='entertainment_list'),
    path('view_entertainment/<int:entertainment_id>/', views.view_entertainment, name='view_entertainment'),
    path('edit_entertainment/<int:entertainment_id>/', views.edit_entertainment, name='edit_entertainment'),
    path('delete_entertainment/<int:entertainment_id>/', views.delete_entertainment, name='delete_entertainment'),
    path('all_entertainments/', views.all_entertainment_list, name='all_entertainment_list'),
    path('catering_home/', views.catering_home, name='catering_home'),
    path('create_catering/', views.create_catering, name='create_catering'),
    path('catering_list/', views.catering_list, name='catering_list'),
    path('edit_catering/<int:catering_id>/', views.edit_catering, name='edit_catering'),
    path('delete_catering/<int:catering_id>/', views.delete_catering, name='delete_catering'),
    path('view_all_catering/', views.view_all_catering, name='view_all_catering'),
    path('view_catering/<int:catering_id>/', views.view_catering, name='view_catering'),
    path('entertainment/<int:entertainment_id>/', views.entertainment_single, name='entertainment_single'),
]
