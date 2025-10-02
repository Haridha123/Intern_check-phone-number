# 🚀 Quick Setup for WhatsApp Checker

## Step 1: Open WhatsApp Web Manually
1. **Open a new Chrome browser window**
2. **Go to https://web.whatsapp.com**
3. **Scan the QR code with your phone** (one time only)
4. **Keep this browser window open**

## Step 2: Start Chrome with Remote Debugging
Close all Chrome windows first, then open Command Prompt and run:
```bash
chrome.exe --remote-debugging-port=9222 --user-data-dir="%USERPROFILE%\whatsapp-chrome"
```

Then navigate to https://web.whatsapp.com and login.

## Step 3: Run the App
```bash
python app.py
```

## 🎯 How It Works
- The app will connect to your existing Chrome browser
- No more QR code scanning needed
- Uses your existing WhatsApp Web session

## 🔧 Troubleshooting
If you get connection errors:
1. Make sure Chrome is running with debugging port
2. Ensure WhatsApp Web is logged in
3. Try refreshing the WhatsApp Web page

## 📱 Alternative: Use Regular Mode
If the above doesn't work, the app will create its own browser session (will ask for QR code once).