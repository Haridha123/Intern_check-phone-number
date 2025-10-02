#!/usr/bin/env python3
"""
WhatsApp Login Setup Script
Run this ONCE to establish WhatsApp Web login session
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def setup_whatsapp_login():
    """Setup WhatsApp Web login session for persistent use"""
    print("🔧 Setting up WhatsApp Web login session...")
    
    # Create Chrome driver with persistent profile
    options = Options()
    profile_dir = os.path.join(os.getcwd(), "chrome_profile")
    
    # Ensure profile directory exists
    if not os.path.exists(profile_dir):
        os.makedirs(profile_dir)
        print(f"📁 Created profile directory: {profile_dir}")
    
    # Chrome options for persistent session
    options.add_argument(f"--user-data-dir={profile_dir}")
    options.add_argument("--profile-directory=WhatsApp")
    options.add_argument("--no-first-run")
    options.add_argument("--disable-default-apps")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-translate")
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-renderer-backgrounding")
    options.add_argument("--disable-backgrounding-occluded-windows")
    
    print("🌐 Opening Chrome with persistent profile...")
    driver = webdriver.Chrome(options=options)
    
    try:
        # Navigate to WhatsApp Web
        print("📱 Loading WhatsApp Web...")
        driver.get("https://web.whatsapp.com")
        
        # Wait for page to load
        wait = WebDriverWait(driver, 10)
        
        # Check if already logged in
        try:
            # Look for chat list (means already logged in)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="chat-list"]')))
            print("✅ Already logged in to WhatsApp Web!")
            return True
        except TimeoutException:
            # Look for QR code (means need to login)
            try:
                qr_code = driver.find_element(By.CSS_SELECTOR, '[data-ref]')
                if qr_code:
                    print("\n📲 QR Code detected!")
                    print("👉 Please scan the QR code with your phone:")
                    print("   1. Open WhatsApp on your phone")
                    print("   2. Go to Settings > Linked Devices") 
                    print("   3. Tap 'Link a Device'")
                    print("   4. Scan the QR code on this screen")
                    print("\n⏳ Waiting for you to scan the QR code...")
                    
                    # Wait for login to complete (QR code disappears)
                    wait_login = WebDriverWait(driver, 120)  # 2 minutes timeout
                    wait_login.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="chat-list"]')))
                    
                    print("✅ Login successful! Session saved.")
                    print("🎉 You can now use the WhatsApp checker without scanning QR code again!")
                    return True
                    
            except TimeoutException:
                print("❌ Login timeout. Please try again.")
                return False
            except Exception as e:
                print(f"❌ Error during login setup: {e}")
                return False
    
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        return False
    
    finally:
        print("🔄 Keeping browser open for 10 seconds to ensure session is saved...")
        time.sleep(10)
        driver.quit()
        print("✅ Setup complete!")

if __name__ == "__main__":
    print("🚀 WhatsApp Login Setup")
    print("=" * 50)
    
    success = setup_whatsapp_login()
    
    if success:
        print("\n✅ Setup completed successfully!")
        print("📱 You can now run the main app without QR scanning:")
        print("   python app.py")
    else:
        print("\n❌ Setup failed. Please try again.")
        print("💡 Make sure you have a stable internet connection.")