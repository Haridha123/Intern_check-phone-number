from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.chrome.options import Options
import time
import os

def create_no_dialog_persistent_driver():
    """Create persistent driver with dialog suppression"""
    # Use your existing profile directory
    profile_dir = r"C:\num\chrome_profile"
    if not os.path.exists(profile_dir):
        os.makedirs(profile_dir)
        print(f"[DEBUG] Created profile directory: {profile_dir}")
    
    options = Options()
    options.add_argument(f"--user-data-dir={profile_dir}")
    options.add_argument("--profile-directory=WhatsApp")
    options.add_argument("--window-size=1200,800")
    
    # Dialog suppression options
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking") 
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions-file-access-check")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    
    # Standard options from your working version
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    
    # Preferences to suppress notifications
    prefs = {
        "profile.default_content_setting_values.notifications": 2,
        "profile.default_content_settings.popups": 0,
        "profile.managed_default_content_settings.popups": 0
    }
    options.add_experimental_option("prefs", prefs)
    
    try:
        driver = webdriver.Chrome(options=options)
        print("[DEBUG] Chrome driver created successfully with dialog suppression")
        return driver
    except Exception as e:
        print(f"[ERROR] Failed to create driver: {e}")
        return None

def initialize_session_no_dialogs(driver):
    """Initialize WhatsApp session (copied from your working version)"""
    try:
        print("[DEBUG] Loading WhatsApp Web...")
        driver.get("https://web.whatsapp.com")
        
        # Wait for either login or QR code
        wait = WebDriverWait(driver, 30)
        
        # Check if already logged in
        try:
            # Look for main WhatsApp interface elements
            chat_elements = [
                "[data-testid=\"chat-list\"]",
                "[data-testid=\"side\"]", 
                "#side",
                "._2Ts6i",  # Side panel
                "._3WByx"   # Chat list
            ]
            
            for element in chat_elements:
                try:
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, element)))
                    print(" Already logged in! Using saved session.")
                    return True
                except TimeoutException:
                    continue
            
        except TimeoutException:
            pass
        
        # If not logged in, check for QR code
        try:
            qr_element = driver.find_element(By.CSS_SELECTOR, "[data-testid=\"qr-code\"], canvas")
            if qr_element:
                print(" QR Code found. Please scan to login.")
                print(" Waiting for login completion...")
                
                # Wait for successful login
                login_wait = WebDriverWait(driver, 120)
                for element in chat_elements:
                    try:
                        login_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, element)))
                        print(" Login successful! Session will be saved.")
                        return True
                    except:
                        continue
        except NoSuchElementException:
            pass
        
        print(" Could not initialize WhatsApp session")
        return False
        
    except Exception as e:
        print(f"[ERROR] Failed to load WhatsApp Web: {e}")
        return False

def check_registration_direct(phone_number, driver):
    """Check if number is registered by trying direct chat URL"""
    try:
        clean_number = phone_number.replace("+", "").replace("-", "").replace(" ", "")
        print(f" Checking registration: {phone_number}")
        
        # Navigate to WhatsApp send URL
        send_url = f"https://web.whatsapp.com/send?phone={clean_number}"
        print(f" Testing URL: {send_url}")
        
        driver.get(send_url)
        time.sleep(6)  # Wait for page load
        
        current_url = driver.current_url
        
        # Check for chat interface elements (indicates registered)
        chat_indicators = [
            "[data-testid=\"conversation-header\"]",
            "[role=\"textbox\"][contenteditable=\"true\"]",
            "[data-testid=\"compose-box-input\"]",
            "._13NKt",  # Message input box
            "[data-testid=\"chat-header\"]"
        ]
        
        for indicator in chat_indicators:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, indicator)
                if elements and any(elem.is_displayed() for elem in elements):
                    print(f" REGISTERED - Found: {indicator}")
                    return True
            except:
                continue
        
        # Check page source for error messages
        page_source = driver.page_source.lower()
        
        error_messages = [
            "phone number shared via url is invalid",
            "invalid phone number",
            "el número de teléfono compartido a través de url no es válido"
        ]
        
        for error in error_messages:
            if error in page_source:
                print(f" NOT REGISTERED - Error: {error}")
                return False
        
        # Check if still on send page (not redirected to chat)
        time.sleep(2)
        final_url = driver.current_url
        
        if "send?phone=" in final_url and "/chat/" not in final_url:
            print(" NOT REGISTERED - No chat redirect")
            return False
        
        # Default to registered if no clear error
        print(" REGISTERED - Chat accessible")
        return True
        
    except Exception as e:
        print(f" Error checking registration: {e}")
        return False

def test_registration_no_dialogs():
    """Test registration checking without dialog boxes"""
    print("  WhatsApp Registration Checker (No Dialogs)")
    print("=" * 50)
    
    # Your test number
    test_number = "+919585914267"
    
    # Create driver
    driver = create_no_dialog_persistent_driver()
    if not driver:
        return
    
    try:
        # Initialize WhatsApp
        if not initialize_session_no_dialogs(driver):
            print(" Failed to initialize WhatsApp session")
            return
        
        print(" WhatsApp session ready")
        print()
        
        # Check registration
        result = check_registration_direct(test_number, driver)
        
        # Display results
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
        
    finally:
        input("\\n  Press Enter to close browser...")
        driver.quit()

if __name__ == "__main__":
    test_registration_no_dialogs()
