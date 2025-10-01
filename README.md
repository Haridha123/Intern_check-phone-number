# WhatsApp Number Checker 📱

A comprehensive WhatsApp registration checker that can verify if phone numbers are registered on WhatsApp. Supports both single number checking and batch processing with persistent login capabilities.

## ✨ Features

- 🔄 **Persistent Login** - Scan QR code once, use forever
- 📊 **Batch Processing** - Check thousands of numbers at once
- 📤 **File Upload** - Support for TXT, CSV, and XLSX files
- 📥 **Export Results** - Download results as CSV or Excel with formatting
- 🌐 **Multiple Interfaces** - Django web app, Flask app, and command line
- ⚡ **Real-time Progress** - Live status updates during batch processing
- 🎯 **High Accuracy** - Multiple detection methods for reliable results

## 🚀 Quick Start

### Prerequisites

- Python 3.7+ installed
- Google Chrome browser
- WhatsApp account on your phone
- Internet connection

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/whatsapp-number-checker.git
   cd whatsapp-number-checker
   ```

2. **Install dependencies**
   ```bash
   pip install selenium django flask pandas openpyxl
   ```

3. **Run the Django web application**
   ```bash
   cd whatsapp_django
   python manage.py runserver
   ```

4. **Open your browser**
   - Visit: http://127.0.0.1:8000
   - First time: Scan QR code with your phone
   - Subsequent uses: No QR scanning needed!

## 🎯 Usage Options

### Web Interface (Recommended)

#### Django App (Full Features)
```bash
cd whatsapp_django
python manage.py runserver
```
- File uploads
- Real-time progress tracking
- Professional exports
- Batch processing

#### Flask App (Simple)
```bash
python app.py
```
- Basic checking interface
- Single/batch number input

### Command Line Tools

#### First-time Setup
```bash
python setup_whatsapp_login.py
```
*One-time QR scan to save your WhatsApp session*

#### Batch Processing
```bash
python batch_checker.py
```
*Process all .txt files in the directory*

#### Single Number Test
```bash
python test_run.py
```
*Quick single number verification*

## 📋 How It Works

1. **Session Setup**: Uses Selenium WebDriver with Chrome to access WhatsApp Web
2. **Persistent Login**: Saves your WhatsApp session in a Chrome profile
3. **Number Verification**: Navigates to WhatsApp send URLs and analyzes the response
4. **Accurate Detection**: Uses multiple methods including:
   - URL redirection analysis
   - Chat interface detection
   - Error message parsing
   - DOM element verification

## 📁 Project Structure

```
├── whatsapp_django/          # Django web application
│   ├── checker/              # Main Django app
│   ├── templates/            # HTML templates
│   └── manage.py             # Django management
├── app.py                    # Flask web application
├── batch_checker.py          # Command line batch processor
├── setup_whatsapp_login.py   # One-time login setup
├── README_Persistent_Login.md # Detailed setup guide
└── templates/                # Flask templates
```

## 🔧 Configuration

### Chrome Profile Storage
- Login sessions are stored in `chrome_profile/`
- Sessions persist across computer restarts
- Delete `chrome_profile/` to reset login

### Session Expiry
- WhatsApp sessions typically last ~2 weeks
- Re-run `setup_whatsapp_login.py` if login expires
- System automatically detects expired sessions

## 📊 Export Formats

### CSV Export
- Basic comma-separated values
- Number, Status, Timestamp

### Excel Export
- Color-coded status indicators
- Professional formatting
- Detailed result information

## ⚠️ Important Notes

### Legal and Ethical Use
- Use responsibly and in compliance with WhatsApp Terms of Service
- Respect privacy and data protection laws
- Only check numbers you have permission to verify

### Rate Limiting
- Built-in delays between checks to avoid detection
- Recommended: Don't exceed 100 numbers per hour
- Use persistent login to minimize authentication requests

### Troubleshooting

#### QR Code Issues
```bash
# Reset login profile
rm -rf chrome_profile/
python setup_whatsapp_login.py
```

#### Browser Crashes
- The persistent profile provides better stability
- Automatic session recovery
- Much less likely to crash during batch processing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is for educational and legitimate business purposes only. Users are responsible for compliance with applicable laws and WhatsApp's Terms of Service.

## 🆘 Support

If you encounter issues:
1. Check the troubleshooting section
2. Ensure Chrome is installed and up to date
3. Verify your internet connection is stable
4. Try resetting the Chrome profile

---

**⚡ Now you can check thousands of numbers without QR code interruptions!**