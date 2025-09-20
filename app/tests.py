from django.test import TestCase
from django.urls import reverse, NoReverseMatch
from .models import Restaurant, Table, Booking
from datetime import date, time
from django.core.management import call_command
from io import StringIO
import os

class TestRestaurantTableBooking(TestCase):
    def setUp(self):
        try:
            self.booking_url = reverse('booking')
        except NoReverseMatch:
            self.booking_url = reverse('app:booking')

        self.restaurant = Restaurant.objects.create(name="Test Diner", location="Fun Zone")
        self.small_table = Table.objects.create(restaurant=self.restaurant, size=2, quantity=1)
        self.large_table = Table.objects.create(restaurant=self.restaurant, size=4, quantity=1)

        self.common_data = {
            'guest_name': 'Alice',
            'guest_email': 'alice@example.com',
            'visit_date': date.today().isoformat(),
            'visit_time': '18:30',
            'restaurant': self.restaurant.id,
        }

    def test_models_str(self):
        self.assertIn("Test Diner", str(self.restaurant))
        self.assertIn("Table for 2", str(self.small_table))
        booking = Booking.objects.create(
            guest_name="Bob",
            guest_email="bob@example.com",
            visit_date=date.today(),
            visit_time=time(19, 0),
            number_of_guests=2,
            restaurant=self.restaurant,
            table=self.small_table
        )
        self.assertIn("Bob", str(booking))

    def test_successful_booking_matches_smallest_table(self):
        post_data = {**self.common_data, 'number_of_guests': 2}
        response = self.client.post(self.booking_url, data=post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'success.html')
        self.assertEqual(Booking.objects.count(), 1)
        booking = Booking.objects.first()
        self.assertEqual(booking.number_of_guests, 2)
        self.assertEqual(booking.table.size, 2)

    def test_overbooking_prevention(self):
        post_data = {**self.common_data, 'number_of_guests': 2}
        self.client.post(self.booking_url, data=post_data)
        self.client.post(self.booking_url, data=post_data)
        resp3 = self.client.post(self.booking_url, data=post_data)
        self.assertContains(resp3, "No tables available at that time.", status_code=200)
        self.assertEqual(Booking.objects.count(), 2)

    def test_booking_larger_party_uses_large_table(self):
        post_data = {**self.common_data, 'number_of_guests': 3}
        response = self.client.post(self.booking_url, data=post_data)
        self.assertEqual(response.status_code, 200)
        booking = Booking.objects.first()
        self.assertEqual(booking.number_of_guests, 3)
        self.assertEqual(booking.table.size, 4)

    def test_invalid_form_missing_fields(self):
        post_data = {
            'guest_name': 'Charlie',
            'visit_date': date.today().isoformat(),
            'visit_time': '19:00',
            'number_of_guests': 2,
            'restaurant': self.restaurant.id,
        }
        response = self.client.post(self.booking_url, data=post_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Booking.objects.count(), 0)
        self.assertFormError(response, 'form', 'guest_email', errors=['This field is required.'])

    def test_get_request_shows_form(self):
        response = self.client.get(self.booking_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<form")
        self.assertIn('form', response.context)

    def test_load_restaurants_command(self):
        csv_content = """restaurant_name,location,table_size,table_count
TestPlace,Zone A,2,3
"""
        path = 'temp_restaurants.csv'
        with open(path, 'w', encoding='utf-8') as f:
            f.write(csv_content)

        out = StringIO()
        call_command('load_restaurants', f'--csv={path}', stdout=out)
        self.assertIn('✅ Done seeding', out.getvalue())

        self.assertTrue(Restaurant.objects.filter(name='TestPlace').exists())
        restaurant = Restaurant.objects.get(name='TestPlace')
        self.assertTrue(Table.objects.filter(restaurant=restaurant, size=2, quantity=3).exists())

        os.remove(path)
