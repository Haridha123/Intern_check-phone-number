from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

def create_silent_driver():
    """Create Chrome driver that runs silently without dialog boxes"""
    chrome_options = Options()
    
    # Headless mode - no visible browser window
    # chrome_options.add_argument("--headless")  # Uncomment for completely invisible
    
    # Suppress notifications and dialog boxes
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-default-apps")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument("--no-default-browser-check")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--disable-features=VizDisplayCompositor")
    
    # Suppress automation detection
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    
    # Use persistent profile (no QR needed after first setup)
    profile_path = r"C:\num\chrome_profile"
    if os.path.exists(profile_path):
        chrome_options.add_argument(f"--user-data-dir={profile_path}")
    
    # Disable logging to reduce console output
    chrome_options.add_argument("--log-level=3")  # Only fatal errors
    chrome_options.add_argument("--silent")
    
    # Set preferences to avoid dialogs
    prefs = {
        "profile.default_content_setting_values": {
            "notifications": 2,  # Block notifications
            "media_stream": 2,   # Block camera/mic access
        },
        "profile.default_content_settings.popups": 0,
        "profile.managed_default_content_settings.popups": 0
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        # Remove automation indicators
        driver.execute_script("Object.defineProperty(navigator, \"webdriver\", {get: () => undefined})")
        print(" Silent Chrome driver created")
        return driver
    except Exception as e:
        print(f" Error creating driver: {e}")
        return None

def initialize_silent_whatsapp(driver):
    """Initialize WhatsApp Web silently"""
    try:
        print(" Loading WhatsApp Web silently...")
        driver.get("https://web.whatsapp.com")
        
        # Wait for either QR code or chat interface
        wait = WebDriverWait(driver, 30)
        
        try:
            # Check if already logged in (look for chat list)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid=\"chat-list\"], [data-testid=\"side\"]")))
            print(" Already logged in - using saved session")
            return True
        except:
            # Check for QR code
            try:
                qr_element = driver.find_element(By.CSS_SELECTOR, "[data-testid=\"qr-code\"], canvas")
                if qr_element:
                    print(" QR Code detected - please scan to login")
                    print(" Waiting for login... (you can scan QR in the browser)")
                    
                    # Wait for successful login
                    wait = WebDriverWait(driver, 120)  # 2 minutes timeout
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid=\"chat-list\"], [data-testid=\"side\"]")))
                    print(" Login successful!")
                    return True
            except:
                pass
        
        print(" Could not initialize WhatsApp Web")
        return False
        
    except Exception as e:
        print(f" Error initializing WhatsApp: {e}")
        return False

def check_registration_silent(phone_number, driver):
    """Check registration silently without dialog boxes"""
    try:
        clean_number = phone_number.replace("+", "").replace("-", "").replace(" ", "")
        print(f" Silently checking: {phone_number}")
        
        # Navigate to WhatsApp send URL
        chat_url = f"https://web.whatsapp.com/send?phone={clean_number}"
        driver.get(chat_url)
        
        # Wait for page load
        time.sleep(6)
        
        current_url = driver.current_url
        
        # Check for chat interface elements (registered)
        try:
            # Look for message input or chat elements
            chat_indicators = [
                "[role=\"textbox\"][contenteditable=\"true\"]",
                "[data-testid=\"compose-box-input\"]",
                "[data-testid=\"conversation-compose-box-input\"]",
                "._13NKt",
                "[data-testid=\"conversation-header\"]"
            ]
            
            for selector in chat_indicators:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements and any(elem.is_displayed() for elem in elements):
                    print(f" REGISTERED - Found: {selector}")
                    return True
        except:
            pass
        
        # Check page source for error messages
        page_source = driver.page_source.lower()
        
        error_indicators = [
            "phone number shared via url is invalid",
            "número de teléfono compartido a través de url no es válido",
            "invalid phone number"
        ]
        
        for error in error_indicators:
            if error in page_source:
                print(" NOT REGISTERED - Error found")
                return False
        
        # Check URL behavior
        if "send?phone=" in current_url:
            # Still on send page, wait a bit more
            time.sleep(3)
            final_url = driver.current_url
            
            if "send?phone=" in final_url and "/chat/" not in final_url:
                print(" NOT REGISTERED - No chat redirect")
                return False
        
        # If we get here, assume registered
        print(" REGISTERED - Chat accessible")
        return True
        
    except Exception as e:
        print(f" Error: {e}")
        return False

def test_silent_checker():
    """Test the silent registration checker"""
    print(" Silent WhatsApp Registration Checker")
    print("=" * 40)
    print(" Running without dialog boxes")
    print(" Minimal browser interaction")
    print()
    
    # Test number
    test_number = "+919585914267"
    
    driver = create_silent_driver()
    if not driver:
        return
    
    try:
        # Initialize WhatsApp
        if not initialize_silent_whatsapp(driver):
            print(" Failed to initialize WhatsApp")
            return
        
        print()
        print(" Starting registration check...")
        
        # Check registration
        result = check_registration_silent(test_number, driver)
        
        # Results
        print()
        print(" RESULT:")
        print("=" * 15)
        print(f" {test_number}")
        status = " REGISTERED" if result else " NOT REGISTERED"
        print(f" {status}")
        
    except Exception as e:
        print(f" Test failed: {e}")
    
    finally:
        print(" Closing browser...")
        if driver:
            driver.quit()
        print(" Done!")

if __name__ == "__main__":
    test_silent_checker()
