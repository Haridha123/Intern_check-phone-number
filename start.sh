#!/bin/bash
cd whatsapp_django
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn whatsapp_django.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --timeout 30