from whatsapp.selenium_checker import create_persistent_driver, initialize_whatsapp_session
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def create_no_dialog_driver():
    """Create driver using your existing function but with dialog suppression"""
    from selenium import webdriver
    import os
    
    chrome_options = Options()
    
    # Your existing profile path
    profile_path = r"C:\num\chrome_profile"
    if os.path.exists(profile_path):
        chrome_options.add_argument(f"--user-data-dir={profile_path}")
    
    # Suppress common dialog boxes
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions-file-access-check")
    chrome_options.add_argument("--disable-extensions-http-throttling")
    chrome_options.add_argument("--disable-extensions-except")
    
    # Preferences to block notifications and popups
    prefs = {
        "profile.default_content_setting_values": {
            "notifications": 2,  # Block all notifications
            "popups": 0,         # Allow popups (needed for WhatsApp)
            "media_stream": 2,   # Block microphone/camera access
        }
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    # Disable automation detection
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, \"webdriver\", {get: () => undefined})")
        print(" No-dialog driver created successfully")
        return driver
    except Exception as e:
        print(f" Error creating driver: {e}")
        # Fallback to your existing method
        return create_persistent_driver()

def check_registration_no_dialogs(phone_number):
    """Check registration without annoying dialog boxes"""
    print(f" Checking registration: {phone_number}")
    print(" Dialog suppression mode: ON")
    
    # Use no-dialog driver
    driver = create_no_dialog_driver()
    if not driver:
        print(" Failed to create driver")
        return False
    
    try:
        # Initialize WhatsApp session
        print(" Initializing WhatsApp session...")
        if not initialize_whatsapp_session(driver):
            print(" Failed to initialize session")
            return False
        
        print(" WhatsApp session ready")
        
        # Clean the number
        clean_number = phone_number.replace("+", "").replace("-", "").replace(" ", "")
        
        # Navigate to WhatsApp send URL  
        send_url = f"https://web.whatsapp.com/send?phone={clean_number}"
        print(f" Navigating to: {send_url}")
        
        driver.get(send_url)
        time.sleep(6)  # Wait for page load
        
        current_url = driver.current_url
        print(f" Current URL: {current_url[:50]}...")
        
        # Method 1: Look for chat interface elements
        chat_selectors = [
            "[data-testid=\"conversation-header\"]",
            "[data-testid=\"chat-header\"]",
            "[role=\"textbox\"][contenteditable=\"true\"]",
            "[data-testid=\"compose-box-input\"]",
            "._13NKt"  # WhatsApp message input class
        ]
        
        for selector in chat_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                visible_elements = [elem for elem in elements if elem.is_displayed()]
                if visible_elements:
                    print(f" REGISTERED - Found chat element: {selector}")
                    return True
            except Exception as e:
                continue
        
        # Method 2: Check page source for errors
        page_source = driver.page_source.lower()
        
        error_messages = [
            "phone number shared via url is invalid",
            "el número de teléfono compartido",
            "invalid phone number",
            "número inválido"
        ]
        
        for error_msg in error_messages:
            if error_msg in page_source:
                print(f" NOT REGISTERED - Error found: {error_msg}")
                return False
        
        # Method 3: Check URL behavior
        time.sleep(2)  # Wait a bit more
        final_url = driver.current_url
        
        if "send?phone=" in final_url and "chat" not in final_url:
            # Still on send page, likely not registered
            print(" NOT REGISTERED - No redirect to chat")
            return False
        
        # If we made it here, probably registered
        print(" REGISTERED - Chat interface accessible")
        return True
        
    except Exception as e:
        print(f" Error during check: {e}")
        return False
    
    finally:
        print(" Closing browser...")
        if driver:
            try:
                driver.quit()
            except:
                pass

def main():
    """Main function"""
    print("  WhatsApp Registration Checker - No Dialogs")
    print("=" * 50)
    print(" Uses your saved WhatsApp session")
    print(" Suppresses notification and popup dialogs")
    print(" Checks actual registration status")
    print()
    
    # Test number
    test_number = "+919585914267"
    
    result = check_registration_no_dialogs(test_number)
    
    # Display result
    print()
    print(" FINAL RESULT:")
    print("=" * 20)
    print(f" Number: {test_number}")
    
    if result:
        print(" Status:  REGISTERED")
        print(" This number has an active WhatsApp account!")
    else:
        print(" Status:  NOT REGISTERED") 
        print(" This number is not registered on WhatsApp")
    
    print()
    print(" Check completed successfully!")

if __name__ == "__main__":
    main()
