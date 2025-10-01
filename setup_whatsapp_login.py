#!/usr/bin/env python3
"""
WhatsApp Login Setup Script
Run this once to set up persistent WhatsApp Web login.
After this, you won't need to scan QR code every time.
"""

from whatsapp.selenium_checker import create_persistent_driver, initialize_whatsapp_session

def setup_persistent_login():
    """Set up persistent WhatsApp Web login"""
    print("🔧 Setting up persistent WhatsApp Web login...")
    print("📝 This needs to be done only once!")
    print("🌐 Make sure you have a stable internet connection!")
    print()
    
    try:
        # Create persistent driver
        print("📱 Creating browser with persistent profile...")
        driver = create_persistent_driver()
        
        # Add extra wait time for slow connections
        print("⏳ Waiting for stable connection...")
        import time
        time.sleep(3)
        
        # Initialize session (will prompt for QR scan if needed)
        if initialize_whatsapp_session(driver):
            print()
            print("✅ SUCCESS! WhatsApp login has been saved.")
            print("🎉 You can now run batch_checker.py without scanning QR code!")
            print()
            print("📋 Next steps:")
            print("  1. Run: python batch_checker.py")
            print("  2. Or run: python test_run.py")
            print("  3. No more QR scanning needed!")
        else:
            print("❌ Failed to set up login. Please try again.")
        
        input("\nPress Enter to close the browser...")
        driver.quit()
        
    except Exception as e:
        print(f"❌ Error setting up login: {e}")

if __name__ == "__main__":
    setup_persistent_login()