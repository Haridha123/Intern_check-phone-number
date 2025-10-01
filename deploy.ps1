# WhatsApp Number Checker - Windows Deployment Script
# PowerShell script for automated deployment on Windows

param(
    [string]$Mode = "dev",
    [switch]$Help
)

# Color functions for better output
function Write-Success { param($Message) Write-Host "✅ $Message" -ForegroundColor Green }
function Write-Warning { param($Message) Write-Host "⚠️  $Message" -ForegroundColor Yellow }
function Write-Error { param($Message) Write-Host "❌ $Message" -ForegroundColor Red }
function Write-Info { param($Message) Write-Host "ℹ️  $Message" -ForegroundColor Cyan }
function Write-Header { param($Message) Write-Host "`n🚀 $Message" -ForegroundColor Blue -BackgroundColor Black }

# Help function
function Show-Help {
    Write-Host @"
WhatsApp Number Checker - Windows Deployment Script

USAGE:
    .\deploy.ps1 [-Mode <mode>] [-Help]

MODES:
    dev         - Development mode (default)
    prod        - Production mode
    docker      - Docker deployment
    service     - Install as Windows service

EXAMPLES:
    .\deploy.ps1                    # Run in development mode
    .\deploy.ps1 -Mode prod         # Run in production mode
    .\deploy.ps1 -Mode docker       # Deploy with Docker
    .\deploy.ps1 -Help              # Show this help

"@ -ForegroundColor White
}

# Check prerequisites
function Test-Prerequisites {
    Write-Header "Checking Prerequisites"
    
    $issues = @()
    
    # Check Python
    try {
        $pythonVersion = python --version 2>&1
        if ($pythonVersion -match "Python 3\.([7-9]|\d{2,})") {
            Write-Success "Python found: $pythonVersion"
        } else {
            $issues += "Python 3.7+ required. Found: $pythonVersion"
        }
    } catch {
        $issues += "Python not found. Please install Python 3.7+"
    }
    
    # Check Chrome
    $chromePaths = @(
        "${env:ProgramFiles}\Google\Chrome\Application\chrome.exe",
        "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe"
    )
    
    $chromeFound = $false
    foreach ($path in $chromePaths) {
        if (Test-Path $path) {
            Write-Success "Chrome found: $path"
            $chromeFound = $true
            break
        }
    }
    
    if (-not $chromeFound) {
        $issues += "Google Chrome not found. Please install Chrome browser."
    }
    
    # Check Git
    try {
        $gitVersion = git --version 2>&1
        Write-Success "Git found: $gitVersion"
    } catch {
        Write-Warning "Git not found. Some features may not work."
    }
    
    if ($issues.Count -gt 0) {
        Write-Error "Prerequisites check failed:"
        foreach ($issue in $issues) {
            Write-Host "  • $issue" -ForegroundColor Red
        }
        return $false
    }
    
    Write-Success "All prerequisites satisfied!"
    return $true
}

# Install Python dependencies
function Install-Dependencies {
    Write-Header "Installing Python Dependencies"
    
    try {
        Write-Info "Upgrading pip..."
        python -m pip install --upgrade pip
        
        Write-Info "Installing project dependencies..."
        python -m pip install -r requirements.txt
        
        Write-Success "Dependencies installed successfully!"
    } catch {
        Write-Error "Failed to install dependencies: $_"
        exit 1
    }
}

# Setup environment
function Initialize-Environment {
    Write-Header "Setting Up Environment"
    
    # Create necessary directories
    $directories = @("logs", "media\results", "static")
    foreach ($dir in $directories) {
        if (-not (Test-Path $dir)) {
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
            Write-Info "Created directory: $dir"
        }
    }
    
    # Setup environment file
    if (-not (Test-Path ".env")) {
        if (Test-Path ".env.example") {
            Copy-Item ".env.example" ".env"
            Write-Success "Created .env file from template"
            Write-Warning "Please edit .env file with your settings"
        }
    }
    
    # Django setup
    Write-Info "Setting up Django..."
    Push-Location "whatsapp_django"
    
    try {
        # Collect static files
        python manage.py collectstatic --noinput
        Write-Success "Static files collected"
        
        # Run migrations
        python manage.py migrate
        Write-Success "Database migrations completed"
    } catch {
        Write-Error "Django setup failed: $_"
    } finally {
        Pop-Location
    }
}

# Development mode
function Start-Development {
    Write-Header "Starting Development Server"
    
    Write-Info "The application will be available at: http://localhost:8000"
    Write-Info "Press Ctrl+C to stop the server"
    Write-Info ""
    
    Push-Location "whatsapp_django"
    try {
        python manage.py runserver 0.0.0.0:8000
    } catch {
        Write-Error "Failed to start development server: $_"
    } finally {
        Pop-Location
    }
}

# Production mode
function Start-Production {
    Write-Header "Starting Production Server"
    
    # Check if gunicorn is installed
    try {
        $gunicornVersion = python -m pip show gunicorn 2>&1
        if (-not $gunicornVersion) {
            Write-Info "Installing Gunicorn..."
            python -m pip install gunicorn
        }
    } catch {
        Write-Info "Installing Gunicorn..."
        python -m pip install gunicorn
    }
    
    Write-Info "The application will be available at: http://localhost:8000"
    Write-Info "Press Ctrl+C to stop the server"
    Write-Info ""
    
    Push-Location "whatsapp_django"
    try {
        python -m gunicorn --bind 0.0.0.0:8000 --workers 2 --timeout 300 whatsapp_django.wsgi:application
    } catch {
        Write-Error "Failed to start production server: $_"
    } finally {
        Pop-Location
    }
}

# Docker deployment
function Start-Docker {
    Write-Header "Docker Deployment"
    
    # Check if Docker is installed
    try {
        $dockerVersion = docker --version 2>&1
        Write-Success "Docker found: $dockerVersion"
    } catch {
        Write-Error "Docker not found. Please install Docker Desktop for Windows."
        return
    }
    
    # Check if docker-compose is available
    try {
        $composeVersion = docker-compose --version 2>&1
        Write-Success "Docker Compose found: $composeVersion"
    } catch {
        Write-Error "Docker Compose not found. Please install Docker Compose."
        return
    }
    
    Write-Info "Building and starting Docker containers..."
    try {
        docker-compose up --build -d
        Write-Success "Docker containers started successfully!"
        Write-Info "Application available at: http://localhost:8000"
        Write-Info "Use 'docker-compose logs -f' to view logs"
        Write-Info "Use 'docker-compose down' to stop containers"
    } catch {
        Write-Error "Docker deployment failed: $_"
    }
}

# Install as Windows service
function Install-Service {
    Write-Header "Installing Windows Service"
    
    Write-Warning "Windows service installation requires additional setup."
    Write-Info "Consider using NSSM (Non-Sucking Service Manager) or similar tools."
    Write-Info "For now, you can run the application manually or use Task Scheduler."
    
    # Create a batch file for service
    $batchContent = @"
@echo off
cd /d "$PWD\whatsapp_django"
python manage.py runserver 0.0.0.0:8000
"@
    
    $batchContent | Out-File -FilePath "start_whatsapp_checker.bat" -Encoding ASCII
    Write-Success "Created start_whatsapp_checker.bat"
    Write-Info "You can use this batch file with Windows Task Scheduler"
}

# Show application status
function Show-Status {
    Write-Header "Application Status"
    
    # Check if Django is running
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000" -Method GET -TimeoutSec 5
        Write-Success "Application is running on http://localhost:8000"
        Write-Info "Response status: $($response.StatusCode)"
    } catch {
        Write-Warning "Application is not responding on http://localhost:8000"
    }
    
    # Check Docker containers if available
    try {
        $containers = docker-compose ps 2>&1
        if ($containers -and $containers -notmatch "error") {
            Write-Info "Docker Containers:"
            Write-Host $containers
        }
    } catch {
        # Docker not available or not running
    }
}

# Main menu for interactive mode
function Show-Menu {
    do {
        Clear-Host
        Write-Header "WhatsApp Number Checker - Windows Deployment"
        Write-Host @"

Select deployment option:

1. 🔧 Quick Development Setup
2. 🚀 Production Setup
3. 🐳 Docker Deployment
4. 📊 Check Status
5. 🔄 Install Dependencies Only
6. ⚙️  Install as Service
7. ❌ Exit

"@ -ForegroundColor White

        $choice = Read-Host "Enter your choice (1-7)"
        
        switch ($choice) {
            "1" {
                if (Test-Prerequisites) {
                    Install-Dependencies
                    Initialize-Environment
                    Start-Development
                }
                break
            }
            "2" {
                if (Test-Prerequisites) {
                    Install-Dependencies
                    Initialize-Environment
                    Start-Production
                }
                break
            }
            "3" {
                Start-Docker
                break
            }
            "4" {
                Show-Status
                Read-Host "Press Enter to continue"
                break
            }
            "5" {
                Install-Dependencies
                Read-Host "Press Enter to continue"
                break
            }
            "6" {
                Install-Service
                Read-Host "Press Enter to continue"
                break
            }
            "7" {
                Write-Success "Goodbye!"
                exit 0
            }
            default {
                Write-Error "Invalid choice. Please select 1-7."
                Start-Sleep -Seconds 2
            }
        }
    } while ($true)
}

# Main execution logic
function Main {
    # Show help if requested
    if ($Help) {
        Show-Help
        return
    }
    
    # Execute based on mode
    switch ($Mode.ToLower()) {
        "dev" {
            if (Test-Prerequisites) {
                Install-Dependencies
                Initialize-Environment
                Start-Development
            }
        }
        "prod" {
            if (Test-Prerequisites) {
                Install-Dependencies
                Initialize-Environment
                Start-Production
            }
        }
        "docker" {
            Start-Docker
        }
        "service" {
            Install-Service
        }
        "menu" {
            Show-Menu
        }
        default {
            Show-Menu
        }
    }
}

# Set execution policy if needed
try {
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
} catch {
    # Ignore if already set or insufficient permissions
}

# Run main function
Main