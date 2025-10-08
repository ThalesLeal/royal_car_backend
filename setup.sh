#!/bin/bash

# Royal Car Wash Backend - Setup Script

echo "🚗 Setting up Royal Car Wash Backend..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9+ first."
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp env.example .env
    echo "✅ .env file created. Please review and update the settings."
fi

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py migrate

# Create superuser
echo "👤 Creating superuser..."
echo "Creating admin user with username 'admin' and password 'admin123'..."
python manage.py shell -c "
from core.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123', first_name='Admin', last_name='User')
    print('✅ Superuser created successfully!')
else:
    print('ℹ️  Superuser already exists.')
"

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "To start the server, run:"
echo "  ./start.sh"
echo ""
echo "Or manually:"
echo "  source venv/bin/activate"
echo "  python manage.py runserver"
echo ""
echo "Admin credentials:"
echo "  Username: admin"
echo "  Password: admin123"
