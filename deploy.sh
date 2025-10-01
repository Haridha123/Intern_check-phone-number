#!/bin/bash

# WhatsApp Number Checker - Automated Deployment Script
# This script handles complete deployment automation

echo "🚀 WhatsApp Number Checker - Automated Deployment"
echo "================================================="

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}$1${NC}"
}

# Check if running on supported OS
check_os() {
    print_header "🔍 Checking Operating System..."
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="linux"
        print_status "Linux detected"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
        print_status "macOS detected"
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
        OS="windows"
        print_status "Windows detected"
    else
        print_error "Unsupported operating system: $OSTYPE"
        exit 1
    fi
}

# Install dependencies
install_dependencies() {
    print_header "📦 Installing Dependencies..."
    
    # Python dependencies
    if command -v python3 &> /dev/null; then
        print_status "Python3 found"
        python3 -m pip install --upgrade pip
        python3 -m pip install -r requirements.txt
    else
        print_error "Python3 not found. Please install Python 3.7+ first."
        exit 1
    fi
    
    # Check for Chrome
    if command -v google-chrome &> /dev/null || command -v chromium-browser &> /dev/null || command -v chrome &> /dev/null; then
        print_status "Chrome browser found"
    else
        print_warning "Chrome browser not found. Installing..."
        install_chrome
    fi
}

# Install Chrome browser
install_chrome() {
    if [[ "$OS" == "linux" ]]; then
        # Install Chrome on Linux
        wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
        echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
        sudo apt update
        sudo apt install -y google-chrome-stable
        
        # Install ChromeDriver
        CHROMEDRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE)
        wget -O /tmp/chromedriver.zip "http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"
        sudo unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
        sudo chmod +x /usr/local/bin/chromedriver
        rm /tmp/chromedriver.zip
        
    elif [[ "$OS" == "macos" ]]; then
        # Install Chrome on macOS using Homebrew
        if command -v brew &> /dev/null; then
            brew install --cask google-chrome
            brew install chromedriver
        else
            print_error "Homebrew not found. Please install Chrome manually."
        fi
        
    else
        print_warning "Please install Google Chrome manually for Windows"
    fi
}

# Setup production environment
setup_production() {
    print_header "🔧 Setting Up Production Environment..."
    
    # Create necessary directories
    mkdir -p logs
    mkdir -p media/results
    mkdir -p static
    
    # Copy environment file
    if [ ! -f .env ]; then
        cp .env.example .env
        print_status "Created .env file from template"
        print_warning "Please edit .env file with your production settings"
    fi
    
    # Django setup
    cd whatsapp_django
    
    # Collect static files
    python3 manage.py collectstatic --noinput
    print_status "Static files collected"
    
    # Run migrations
    python3 manage.py migrate
    print_status "Database migrations completed"
    
    cd ..
}

# Start the application
start_application() {
    print_header "🚀 Starting WhatsApp Number Checker..."
    
    # Choose deployment method
    echo "Select deployment method:"
    echo "1) Development Server (localhost:8000)"
    echo "2) Production with Gunicorn"
    echo "3) Docker Container"
    echo "4) Exit"
    
    read -p "Enter your choice (1-4): " choice
    
    case $choice in
        1)
            print_status "Starting development server..."
            cd whatsapp_django
            python3 manage.py runserver 0.0.0.0:8000
            ;;
        2)
            print_status "Starting production server with Gunicorn..."
            cd whatsapp_django
            gunicorn --bind 0.0.0.0:8000 --workers 3 --timeout 300 whatsapp_django.wsgi:application
            ;;
        3)
            print_status "Building and starting Docker container..."
            docker-compose up --build
            ;;
        4)
            print_status "Goodbye!"
            exit 0
            ;;
        *)
            print_error "Invalid choice. Please select 1-4."
            start_application
            ;;
    esac
}

# Create systemd service for production
create_service() {
    print_header "⚙️ Creating System Service..."
    
    if [[ "$OS" == "linux" ]]; then
        # Create systemd service file
        sudo tee /etc/systemd/system/whatsapp-checker.service > /dev/null <<EOF
[Unit]
Description=WhatsApp Number Checker
After=network.target

[Service]
Type=exec
User=$USER
WorkingDirectory=$(pwd)/whatsapp_django
Environment=PATH=$(pwd)/.venv/bin
ExecStart=/usr/local/bin/gunicorn --bind 0.0.0.0:8000 --workers 3 whatsapp_django.wsgi:application
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF
        
        # Enable and start service
        sudo systemctl daemon-reload
        sudo systemctl enable whatsapp-checker.service
        sudo systemctl start whatsapp-checker.service
        
        print_status "System service created and started"
        print_status "Use 'sudo systemctl status whatsapp-checker' to check status"
    else
        print_warning "System service creation is only supported on Linux"
    fi
}

# Setup Nginx reverse proxy
setup_nginx() {
    print_header "🌐 Setting Up Nginx Reverse Proxy..."
    
    if [[ "$OS" == "linux" ]]; then
        # Install Nginx
        sudo apt update
        sudo apt install -y nginx
        
        # Create Nginx configuration
        sudo tee /etc/nginx/sites-available/whatsapp-checker > /dev/null <<EOF
server {
    listen 80;
    server_name your-domain.com;  # Replace with your domain
    
    client_max_body_size 10M;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_read_timeout 300;
        proxy_connect_timeout 300;
        proxy_send_timeout 300;
    }
    
    location /static/ {
        alias $(pwd)/whatsapp_django/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }
    
    location /media/ {
        alias $(pwd)/whatsapp_django/media/;
        expires 7d;
        add_header Cache-Control "public, no-transform";
    }
}
EOF
        
        # Enable site
        sudo ln -sf /etc/nginx/sites-available/whatsapp-checker /etc/nginx/sites-enabled/
        sudo nginx -t
        sudo systemctl restart nginx
        
        print_status "Nginx reverse proxy configured"
        print_warning "Update server_name in /etc/nginx/sites-available/whatsapp-checker with your domain"
    else
        print_warning "Nginx setup is only supported on Linux"
    fi
}

# SSL Certificate setup
setup_ssl() {
    print_header "🔒 Setting Up SSL Certificate..."
    
    if [[ "$OS" == "linux" ]]; then
        # Install Certbot
        sudo apt install -y certbot python3-certbot-nginx
        
        read -p "Enter your domain name: " domain
        if [ ! -z "$domain" ]; then
            sudo certbot --nginx -d $domain
            print_status "SSL certificate installed for $domain"
        else
            print_warning "No domain provided. SSL setup skipped."
        fi
    else
        print_warning "SSL setup is only supported on Linux"
    fi
}

# Main deployment menu
main_menu() {
    print_header "🎯 WhatsApp Number Checker - Deployment Options"
    echo ""
    echo "1) Quick Setup (Development)"
    echo "2) Production Setup (VPS/Server)"
    echo "3) Docker Deployment"
    echo "4) Create System Service"
    echo "5) Setup Nginx Reverse Proxy"
    echo "6) Setup SSL Certificate"
    echo "7) Complete Production Setup (All-in-one)"
    echo "8) Check Application Status"
    echo "9) Exit"
    echo ""
    
    read -p "Enter your choice (1-9): " main_choice
    
    case $main_choice in
        1)
            install_dependencies
            setup_production
            start_application
            ;;
        2)
            install_dependencies
            setup_production
            create_service
            ;;
        3)
            print_status "Starting Docker deployment..."
            docker-compose up --build -d
            print_status "Docker containers started"
            print_status "Access the application at: http://localhost:8000"
            ;;
        4)
            create_service
            ;;
        5)
            setup_nginx
            ;;
        6)
            setup_ssl
            ;;
        7)
            install_dependencies
            setup_production
            create_service
            setup_nginx
            setup_ssl
            print_status "Complete production setup finished!"
            ;;
        8)
            print_header "📊 Application Status"
            if command -v systemctl &> /dev/null; then
                sudo systemctl status whatsapp-checker.service
            fi
            if command -v docker &> /dev/null; then
                docker-compose ps
            fi
            ;;
        9)
            print_status "Goodbye!"
            exit 0
            ;;
        *)
            print_error "Invalid choice. Please select 1-9."
            main_menu
            ;;
    esac
}

# Main execution
main() {
    clear
    print_header "🚀 WhatsApp Number Checker - Automated Deployment System"
    print_header "============================================================"
    echo ""
    
    check_os
    main_menu
}

# Run main function
main "$@"