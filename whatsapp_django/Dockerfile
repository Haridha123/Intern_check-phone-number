# Use a slim Python base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set work directory
WORKDIR /app

# Install system dependencies for psycopg2 and Django
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        gcc \
        wget \
        gnupg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome for Selenium (needed for WhatsApp checking functionality)
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Collect static files if Django settings exist
RUN if [ -f "whatsapp_django/settings.py" ]; then python manage.py collectstatic --noinput; fi

# Expose port
EXPOSE 8000

# Use Gunicorn to run the Django app
# Automatically infer the project name for the WSGI module
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:8000 --workers 3 whatsapp_django.wsgi:application"]