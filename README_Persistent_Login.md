# WhatsApp Number Checker with Persistent Login

## 🔄 No More QR Code Scanning Every Time!

This project now supports **persistent login** - you only need to scan the QR code **once**, and then the browser will remember your login session.

## 📋 Quick Start Guide

### 1. First Time Setup (One-time only)
```bash
python setup_whatsapp_login.py
```
- Scan QR code when prompted
- Login session will be saved
- You won't need to scan again!

### 2. Check Single Number
```bash
python test_run.py
```
- Uses saved login session
- No QR scanning needed
- Quick single number check

### 3. Batch Check Multiple Numbers
```bash
python batch_checker.py
```
- Uses saved login session
- Processes all .txt files
- No QR scanning needed

## 🗂️ How Persistent Login Works

### Profile Storage
- Login data saved in: `C:\num\chrome_profile\`
- WhatsApp session cookies stored
- Browser remembers your login

### Benefits
- ✅ **One-time setup** - scan QR code only once
- ✅ **Faster startup** - no waiting for QR scan
- ✅ **Batch processing** - check hundreds of numbers without interruption
- ✅ **Session persistence** - works even after computer restart

### File Structure
```
C:\num\
├── chrome_profile\          # 🔒 Persistent browser profile (auto-created)
├── whatsapp\
│   ├── selenium_checker.py  # ⚡ Enhanced with persistent login
│   └── utils.py
├── setup_whatsapp_login.py  # 🔧 One-time setup script
├── batch_checker.py         # 📊 Batch processing (no QR needed)
├── test_run.py             # 🧪 Single test (no QR needed)
└── numbers*.txt            # 📞 Your number files
```

## 🚨 Important Notes

### If Login Expires
- WhatsApp sessions can expire after ~2 weeks of inactivity
- Simply run `setup_whatsapp_login.py` again to re-login
- The system will automatically detect if you need to re-scan

### Security
- Profile data is stored locally only
- No data sent to external servers
- Delete `chrome_profile\` folder to reset login

## 🔧 Troubleshooting

### "QR code detected" message
- This means you need to login again
- Follow the on-screen instructions
- Scan QR code with your phone

### Profile not working
```bash
# Delete profile and start fresh
rmdir /s C:\num\chrome_profile
python setup_whatsapp_login.py
```

### Browser crashes
- The persistent profile is more stable
- Session recovery is automatic
- Much less likely to crash during batch processing

---

**Now you can check thousands of numbers without any QR code interruptions! 🎉**