from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time

def setup_persistent_session():
    print("🔄 Setting up persistent WhatsApp session...")
    
    # Create chrome_profile directory if it doesn't exist
    profile_dir = os.path.join(os.getcwd(), 'chrome_profile')
    if not os.path.exists(profile_dir):
        os.makedirs(profile_dir)
    
    # Set up Chrome options for persistent session
    options = Options()
    options.add_argument(f'--user-data-dir={profile_dir}')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument("--window-size=1200,800")
    
    try:
        driver = webdriver.Chrome(options=options)
        driver.get('https://web.whatsapp.com')
        
        print("\n📱 Please scan the QR code in the browser window")
        print("⚠️ IMPORTANT: Keep the browser window open until WhatsApp Web fully loads!")
        print("💡 After scanning, wait until you see your chats loaded.")
        
        input("\n👉 Press Enter after WhatsApp Web is fully loaded with your chats visible...")
        print("\n✅ Session saved! You can now close this window and run the Django server.")
        
        time.sleep(2)
        driver.quit()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    setup_persistent_session()