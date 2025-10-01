#!/usr/bin/env bash
# Render.com build script

set -o errexit  # exit on error

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Setting up Django..."
cd whatsapp_django
echo "Collecting static files..."
python manage.py collectstatic --no-input
echo "Running migrations..."
python manage.py migrate

echo "Build completed successfully!"