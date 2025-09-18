@echo off
echo Starting Restaurant Table Booking App...
echo.

REM Check if Python is available
py -3.12 --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python 3.12 not found. Please install Python 3.12 or higher.
    pause
    exit /b 1
)

REM Install Django if not already installed
echo Installing Django...
py -3.12 -m pip install Django

REM Run migrations
echo Running database migrations...
py -3.12 manage.py migrate

REM Load sample data if database is empty
echo Loading sample restaurant data...
py -3.12 manage.py load_restaurants

REM Create superuser if it doesn't exist
echo Creating admin user...
py -3.12 manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin123')"

REM Start the development server
echo.
echo Starting development server...
echo.
echo ========================================
echo Restaurant Table Booking App is running!
echo ========================================
echo.
echo Main App:     http://127.0.0.1:8000/
echo Admin Panel:  http://127.0.0.1:8000/admin/
echo.
echo Admin Login:
echo Username: admin
echo Password: admin123
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

py -3.12 manage.py runserver
