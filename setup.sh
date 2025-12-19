#!/bin/bash

echo "========================================="
echo "Cars Dealership - Setup Script"
echo "========================================="
echo ""

# Navigate to server directory
cd server

echo "Step 1: Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "Step 2: Running database migrations..."
python manage.py migrate

echo ""
echo "Step 3: Creating superuser (admin/admin123)..."
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin123') if not User.objects.filter(username='admin').exists() else print('Superuser already exists')" | python manage.py shell

echo ""
echo "Step 4: Populating sample data..."
python manage.py populate_data

echo ""
echo "Step 5: Creating test user (testuser/testpass123)..."
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_user('testuser', 'test@example.com', 'testpass123') if not User.objects.filter(username='testuser').exists() else print('Test user already exists')" | python manage.py shell

echo ""
echo "========================================="
echo "Setup Complete!"
echo "========================================="
echo ""
echo "To start the Django server:"
echo "  cd server"
echo "  python manage.py runserver"
echo ""
echo "To start the sentiment analyzer:"
echo "  cd server/sentiment_analyzer"
echo "  python app.py"
echo ""
echo "Admin credentials:"
echo "  Username: admin"
echo "  Password: admin123"
echo ""
echo "Test user credentials:"
echo "  Username: testuser"
echo "  Password: testpass123"
echo ""
echo "Admin panel: http://localhost:8000/admin/"
echo "Application: http://localhost:8000/"
echo "========================================="