from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

def create_stable_driver():
    """Create a stable Chrome driver with minimal dialog boxes"""
    chrome_options = Options()
    
    # Essential options to suppress dialogs
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking") 
    chrome_options.add_argument("--disable-default-apps")
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument("--no-default-browser-check")
    chrome_options.add_argument("--disable-infobars")
    
    # Keep browser stable
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    
    # Use saved profile for no QR scanning
    profile_path = r"C:\num\chrome_profile"
    if os.path.exists(profile_path):
        chrome_options.add_argument(f"--user-data-dir={profile_path}")
        print(f" Using saved profile: {profile_path}")
    
    # Notification preferences
    prefs = {
        "profile.default_content_setting_values.notifications": 2,
        "profile.default_content_settings.popups": 0
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        print(" Stable driver created")
        return driver
    except Exception as e:
        print(f" Driver error: {e}")
        return None

def check_number_simple(phone_number):
    """Simple registration check"""
    print(f" Checking: {phone_number}")
    print(" No dialog boxes mode activated")
    
    driver = create_stable_driver()
    if not driver:
        return False
    
    try:
        # Load WhatsApp Web
        print(" Loading WhatsApp Web...")
        driver.get("https://web.whatsapp.com")
        time.sleep(5)
        
        # Check if already logged in
        try:
            # Look for chat list or main interface
            wait = WebDriverWait(driver, 20)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid=\"chat-list\"], [data-testid=\"side\"], #side")))
            print(" Logged in successfully")
        except:
            print(" Please scan QR code if it appears...")
            # Give time for manual QR scan
            time.sleep(15)
        
        # Now test the registration
        clean_number = phone_number.replace("+", "").replace(" ", "").replace("-", "")
        test_url = f"https://web.whatsapp.com/send?phone={clean_number}"
        
        print(f" Testing URL: {test_url}")
        driver.get(test_url)
        
        # Wait for page to load
        time.sleep(8)
        
        # Check what happened
        current_url = driver.current_url
        page_source = driver.page_source.lower()
        
        print(f" Current URL: {current_url[:60]}...")
        
        # Look for positive indicators (registered)
        positive_indicators = [
            "[data-testid=\"conversation-header\"]",
            "[role=\"textbox\"]", 
            "[contenteditable=\"true\"]",
            "._13NKt"
        ]
        
        found_chat = False
        for indicator in positive_indicators:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, indicator)
                if elements and any(elem.is_displayed() for elem in elements):
                    print(f" REGISTERED - Found chat element: {indicator}")
                    found_chat = True
                    break
            except:
                continue
        
        if found_chat:
            return True
        
        # Check for error messages
        error_phrases = [
            "phone number shared via url is invalid",
            "invalid phone",
            "not registered"
        ]
        
        for phrase in error_phrases:
            if phrase in page_source:
                print(f" NOT REGISTERED - Error: {phrase}")
                return False
        
        # Check URL patterns
        if "send?phone=" in current_url and "chat" not in current_url:
            print(" NOT REGISTERED - Still on send page")
            return False
        
        # Default to registered if no clear error
        print(" REGISTERED - Accessible")
        return True
        
    except Exception as e:
        print(f" Error: {e}")
        return False
    
    finally:
        print(" Closing browser...")
        driver.quit()

def main():
    """Main test function"""
    print(" Stable WhatsApp Checker (Minimal Dialogs)")
    print("=" * 45)
    
    # Test your number
    test_number = "+919585914267"
    
    result = check_number_simple(test_number)
    
    print("\\n FINAL RESULT:")
    print("=" * 20)
    print(f" Number: {test_number}")
    status = " REGISTERED" if result else " NOT REGISTERED"  
    print(f" Status: {status}")
    
    if result:
        print(" This number has a WhatsApp account!")
    else:
        print(" This number is not on WhatsApp")

if __name__ == "__main__":
    main()
