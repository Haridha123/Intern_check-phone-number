#!/bin/bash
# Quick deployment script for your WhatsApp Checker

echo "🚀 Deploying WhatsApp Number Checker from GitHub..."

# Clone repository
git clone https://github.com/Haridha123/Intern_check-phone-number.git
cd Intern_check-phone-number

# Install Python dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Setup Django
echo "🔧 Setting up Django..."
cd whatsapp_django
python manage.py collectstatic --noinput
python manage.py migrate

# Start server
echo "🚀 Starting server..."
echo "Application will be available at: http://localhost:8000"
python manage.py runserver 0.0.0.0:8000