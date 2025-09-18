from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Restaurant, Table, Booking
from django import forms
import datetime

class BookingForm(forms.Form):
    guest_name = forms.CharField(
        max_length=100, 
        label="Guest name",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'})
    )
    guest_email = forms.EmailField(
        label="Guest email",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'})
    )
    guest_phone = forms.CharField(
        max_length=20, 
        required=False,
        label="Phone number (optional)",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'})
    )
    visit_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date', 
            'min': datetime.date.today().isoformat(),
            'class': 'form-control'
        }),
        label="Visit date"
    )
    visit_time = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'type': 'time', 
            'step': '900',
            'class': 'form-control'
        }),
        label="Visit time"
    )
    number_of_guests = forms.IntegerField(
        min_value=1, 
        max_value=20,
        label="Number of guests",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'How many people?'})
    )
    restaurant = forms.ModelChoiceField(
        queryset=Restaurant.objects.filter(is_active=True),
        empty_label="-- Choose a Restaurant --",
        label="Restaurant",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    special_requests = forms.CharField(
        required=False,
        label="Special requests (optional)",
        widget=forms.Textarea(attrs={
            'class': 'form-control', 
            'rows': 3, 
            'placeholder': 'Any special dietary requirements or requests?'
        })
    )

    def clean_visit_date(self):
        date = self.cleaned_data.get('visit_date')
        if date and date < datetime.date.today():
            raise forms.ValidationError("Cannot book for past dates.")
        return date

    def clean_number_of_guests(self):
        guests = self.cleaned_data.get('number_of_guests')
        if guests and guests > 20:
            raise forms.ValidationError("Maximum 20 guests per booking.")
        return guests

def index(request):
    """Main booking page"""
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            party_size = data['number_of_guests']
            selected_restaurant = data['restaurant']
            visit_date = data['visit_date']
            visit_time = data['visit_time']

            # Check if booking is not in the past
            booking_datetime = timezone.datetime.combine(visit_date, visit_time)
            if booking_datetime < timezone.now().replace(tzinfo=None):
                form.add_error(None, "Cannot book for past times.")
            else:
                # Find available tables
                tables = Table.objects.filter(
                    restaurant=selected_restaurant,
                    size__gte=party_size,
                    is_active=True
                ).order_by('size')

                for table in tables:
                    with transaction.atomic():
                        existing_count = Booking.objects.filter(
                            table=table,
                            visit_date=visit_date,
                            visit_time=visit_time,
                            status='confirmed'
                        ).count()

                        if existing_count < table.quantity:
                            booking = Booking.objects.create(
                                guest_name=data['guest_name'],
                                guest_email=data['guest_email'],
                                guest_phone=data.get('guest_phone', ''),
                                visit_date=visit_date,
                                visit_time=visit_time,
                                number_of_guests=party_size,
                                restaurant=selected_restaurant,
                                table=table,
                                special_requests=data.get('special_requests', '')
                            )
                            messages.success(request, f"Booking confirmed! Your booking ID is {booking.id}")
                            return render(request, 'success.html', {
                                'booking': booking,
                                'booking_url': request.path
                            })
                
                form.add_error(None, "No tables available at that time. Please try a different time or date.")
    else:
        form = BookingForm()
    
    # Get featured restaurants for display
    featured_restaurants = Restaurant.objects.filter(is_active=True)[:3]
    
    return render(request, 'booking_template.html', {
        'form': form,
        'featured_restaurants': featured_restaurants
    })

def booking_detail(request, booking_id):
    """View booking details"""
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'booking_detail.html', {'booking': booking})

def cancel_booking(request, booking_id):
    """Cancel a booking"""
    booking = get_object_or_404(Booking, id=booking_id)
    
    if not booking.can_be_cancelled():
        messages.error(request, "This booking cannot be cancelled.")
        return redirect('booking_detail', booking_id=booking_id)
    
    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, "Booking cancelled successfully.")
        return redirect('index')
    
    return render(request, 'cancel_booking.html', {'booking': booking})

def restaurant_list(request):
    """List all restaurants"""
    restaurants = Restaurant.objects.filter(is_active=True)
    paginator = Paginator(restaurants, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'restaurant_list.html', {'page_obj': page_obj})

def restaurant_detail(request, restaurant_id):
    """View restaurant details"""
    restaurant = get_object_or_404(Restaurant, id=restaurant_id, is_active=True)
    tables = restaurant.tables.filter(is_active=True)
    
    return render(request, 'restaurant_detail.html', {
        'restaurant': restaurant,
        'tables': tables
    })

def check_availability(request):
    """AJAX endpoint to check table availability"""
    if request.method == 'GET':
        restaurant_id = request.GET.get('restaurant_id')
        date = request.GET.get('date')
        time = request.GET.get('time')
        guests = request.GET.get('guests')
        
        if not all([restaurant_id, date, time, guests]):
            return JsonResponse({'error': 'Missing parameters'}, status=400)
        
        try:
            restaurant = Restaurant.objects.get(id=restaurant_id, is_active=True)
            tables = Table.objects.filter(
                restaurant=restaurant,
                size__gte=int(guests),
                is_active=True
            ).order_by('size')
            
            available_tables = []
            for table in tables:
                existing_count = Booking.objects.filter(
                    table=table,
                    visit_date=date,
                    visit_time=time,
                    status='confirmed'
                ).count()
                
                if existing_count < table.quantity:
                    available_tables.append({
                        'id': table.id,
                        'size': table.size,
                        'available': table.quantity - existing_count
                    })
            
            return JsonResponse({
                'available': len(available_tables) > 0,
                'tables': available_tables
            })
            
        except (Restaurant.DoesNotExist, ValueError):
            return JsonResponse({'error': 'Invalid parameters'}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)
