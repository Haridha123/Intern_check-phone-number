#!/usr/bin/env bash
# Render.com build script

set -o errexit  # exit on error

pip install --upgrade pip
pip install -r requirements.txt

cd whatsapp_django
python manage.py collectstatic --no-input
python manage.py migrate