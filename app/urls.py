from django.urls import path
from .views import (
    index, booking_detail, cancel_booking, 
    restaurant_list, restaurant_detail, check_availability
)

app_name = 'app'

urlpatterns = [
    path('', index, name='index'),
    path('booking/', index, name='booking'),
    path('booking/<uuid:booking_id>/', booking_detail, name='booking_detail'),
    path('booking/<uuid:booking_id>/cancel/', cancel_booking, name='cancel_booking'),
    path('restaurants/', restaurant_list, name='restaurant_list'),
    path('restaurants/<int:restaurant_id>/', restaurant_detail, name='restaurant_detail'),
    path('api/check-availability/', check_availability, name='check_availability'),
]
