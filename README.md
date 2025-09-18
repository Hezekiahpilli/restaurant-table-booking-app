# Restaurant Table Booking App

A modern, responsive web application for booking restaurant tables built with Django.

## Features

### 🍽️ **Restaurant Management**
- Browse available restaurants
- View restaurant details, contact information, and hours
- Restaurant-specific table configurations

### 📅 **Table Booking System**
- Real-time table availability checking
- Easy booking form with validation
- Support for special requests
- Booking confirmation with unique ID

### 👥 **Booking Management**
- View booking details
- Cancel bookings (if not in the past)
- Booking status tracking (Confirmed, Cancelled, Completed, No Show)

### 🎨 **Modern UI/UX**
- Responsive design that works on all devices
- Beautiful gradient backgrounds and modern styling
- Interactive elements with smooth animations
- Font Awesome icons throughout

### ⚙️ **Admin Interface**
- Comprehensive Django admin interface
- Manage restaurants, tables, and bookings
- Bulk actions for booking management
- Advanced filtering and search capabilities

## Quick Start

### Prerequisites
- Python 3.12+ (recommended)
- pip (Python package installer)

### Installation

1. **Clone or download the project**
   ```bash
   cd restaurant_table_booking_app
   ```

2. **Install dependencies**
   ```bash
   py -3.12 -m pip install Django
   ```

3. **Set up the database**
   ```bash
   py -3.12 manage.py makemigrations
   py -3.12 manage.py migrate
   ```

4. **Load sample data**
   ```bash
   py -3.12 manage.py load_restaurants
   ```

5. **Create admin user (optional)**
   ```bash
   py -3.12 manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   py -3.12 manage.py runserver
   ```

7. **Open your browser**
   - Main app: http://127.0.0.1:8000/
   - Admin interface: http://127.0.0.1:8000/admin/

## Usage

### For Customers
1. **Browse Restaurants**: Visit the restaurants page to see all available dining options
2. **Book a Table**: Use the main booking form to make a reservation
3. **View Booking**: Use your booking ID to view or cancel your reservation
4. **Special Requests**: Add any dietary requirements or special requests during booking

### For Administrators
1. **Access Admin**: Go to `/admin/` and log in with your superuser credentials
2. **Manage Restaurants**: Add, edit, or deactivate restaurants
3. **Configure Tables**: Set up table sizes and quantities for each restaurant
4. **Monitor Bookings**: View, filter, and manage all bookings
5. **Update Status**: Change booking statuses (Confirmed, Cancelled, Completed, No Show)

## Project Structure

```
restaurant_table_booking_app/
├── app/                    # Main Django app
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── urls.py            # URL patterns
│   ├── admin.py           # Admin interface configuration
│   └── management/        # Custom management commands
├── main/                  # Django project settings
│   ├── settings.py        # Project configuration
│   └── urls.py            # Main URL configuration
├── templates/             # HTML templates
│   ├── base.html          # Base template
│   ├── booking_template.html
│   ├── success.html
│   ├── booking_detail.html
│   ├── cancel_booking.html
│   ├── restaurant_list.html
│   └── restaurant_detail.html
├── static/                # Static files
│   └── css/
│       └── style.css      # Main stylesheet
├── restaurants.csv        # Sample restaurant data
├── requirements.txt       # Python dependencies
└── manage.py             # Django management script
```

## Key Features Explained

### Real-time Availability Checking
The app includes AJAX-powered real-time table availability checking. As users select a restaurant, date, time, and party size, the system automatically checks if tables are available and provides immediate feedback.

### Responsive Design
The application is fully responsive and works seamlessly on:
- Desktop computers
- Tablets
- Mobile phones

### Booking Management
- **Unique Booking IDs**: Each booking gets a UUID for easy reference
- **Status Tracking**: Track booking status from confirmation to completion
- **Cancellation Policy**: Users can cancel bookings if they haven't passed
- **Special Requests**: Support for dietary requirements and special needs

### Admin Features
- **Bulk Actions**: Select multiple bookings and change their status
- **Advanced Filtering**: Filter by date, restaurant, status, etc.
- **Search**: Search across all booking fields
- **Export Capabilities**: Built-in Django admin export features

## Customization

### Adding New Restaurants
1. Use the admin interface to add restaurants manually, or
2. Update the `restaurants.csv` file and run `load_restaurants` command

### Styling
- Modify `static/css/style.css` to change the appearance
- The app uses CSS custom properties (variables) for easy color theming

### Business Logic
- Modify `app/models.py` to add new fields or change validation rules
- Update `app/views.py` to change booking logic or add new features

## Technical Details

- **Framework**: Django 4.2+
- **Database**: SQLite (default, easily configurable for PostgreSQL/MySQL)
- **Frontend**: HTML5, CSS3, JavaScript (jQuery)
- **Icons**: Font Awesome 6.0
- **Responsive**: CSS Grid and Flexbox

## Troubleshooting

### Common Issues

1. **Django not found**: Make sure you're using the correct Python version
   ```bash
   py -3.12 manage.py runserver
   ```

2. **Database errors**: Run migrations again
   ```bash
   py -3.12 manage.py migrate
   ```

3. **Static files not loading**: Collect static files
   ```bash
   py -3.12 manage.py collectstatic
   ```

4. **No restaurants showing**: Load sample data
   ```bash
   py -3.12 manage.py load_restaurants
   ```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

---

**Enjoy your restaurant booking experience! 🍽️✨**
