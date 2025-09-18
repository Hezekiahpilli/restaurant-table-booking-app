from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid

class Restaurant(models.Model):
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    opening_hours = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Table(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='tables')
    size = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)])
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['restaurant', 'size']
        unique_together = ['restaurant', 'size']

    def __str__(self):
        return f"{self.restaurant.name} - Table for {self.size} (x{self.quantity})"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
        ('no_show', 'No Show'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    guest_name = models.CharField(max_length=100)
    guest_email = models.EmailField()
    guest_phone = models.CharField(max_length=20, blank=True, null=True)
    visit_date = models.DateField()
    visit_time = models.TimeField()
    number_of_guests = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)])
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='bookings')
    table = models.ForeignKey(Table, on_delete=models.CASCADE, null=True, blank=True, related_name='bookings')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
    special_requests = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return (f"{self.guest_name} at {self.restaurant.name} on {self.visit_date} {self.visit_time} "
                f"(party of {self.number_of_guests})")

    @property
    def is_past_booking(self):
        """Check if the booking is in the past"""
        now = timezone.now()
        booking_datetime = timezone.datetime.combine(self.visit_date, self.visit_time)
        return booking_datetime < now.replace(tzinfo=None)

    def can_be_cancelled(self):
        """Check if booking can be cancelled (not in past and not already cancelled)"""
        return not self.is_past_booking and self.status == 'confirmed'
