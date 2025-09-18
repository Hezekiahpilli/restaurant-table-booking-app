from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Restaurant, Table, Booking

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'phone', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'location', 'phone', 'email']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'location', 'description')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email', 'opening_hours')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ['restaurant', 'size', 'quantity', 'is_active', 'created_at']
    list_filter = ['is_active', 'restaurant', 'size', 'created_at']
    search_fields = ['restaurant__name', 'size']
    list_editable = ['is_active', 'quantity']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Table Information', {
            'fields': ('restaurant', 'size', 'quantity')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = [
        'guest_name', 'restaurant', 'visit_date', 'visit_time', 
        'number_of_guests', 'status', 'created_at'
    ]
    list_filter = ['status', 'visit_date', 'restaurant', 'created_at']
    search_fields = ['guest_name', 'guest_email', 'guest_phone', 'restaurant__name']
    list_editable = ['status']
    readonly_fields = ['id', 'created_at', 'updated_at', 'booking_link']
    date_hierarchy = 'visit_date'
    
    fieldsets = (
        ('Booking Information', {
            'fields': ('id', 'guest_name', 'guest_email', 'guest_phone')
        }),
        ('Reservation Details', {
            'fields': ('restaurant', 'table', 'visit_date', 'visit_time', 'number_of_guests')
        }),
        ('Status & Requests', {
            'fields': ('status', 'special_requests')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('Actions', {
            'fields': ('booking_link',),
            'classes': ('collapse',)
        }),
    )
    
    def booking_link(self, obj):
        if obj.id:
            url = reverse('admin:app_booking_change', args=[obj.id])
            return format_html('<a href="{}">View in Detail</a>', url)
        return '-'
    booking_link.short_description = 'Admin Link'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('restaurant', 'table')
    
    actions = ['mark_confirmed', 'mark_cancelled', 'mark_completed']
    
    def mark_confirmed(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(request, f'{updated} bookings marked as confirmed.')
    mark_confirmed.short_description = 'Mark selected bookings as confirmed'
    
    def mark_cancelled(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} bookings marked as cancelled.')
    mark_cancelled.short_description = 'Mark selected bookings as cancelled'
    
    def mark_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} bookings marked as completed.')
    mark_completed.short_description = 'Mark selected bookings as completed'

# Customize admin site
admin.site.site_header = "Restaurant Table Booking Administration"
admin.site.site_title = "Booking Admin"
admin.site.index_title = "Welcome to Restaurant Booking Administration"
