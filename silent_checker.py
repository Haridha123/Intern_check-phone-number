from whatsapp.selenium_checker import create_persistent_driver, initialize_whatsapp_session
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time
import os

def create_silent_driver():
    """Create Chrome driver that runs silently without dialogs"""
    chrome_options = Options()
    
    # Headless mode - no visible browser window
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Suppress all dialogs and notifications
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-default-apps")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--disable-features=VizDisplayCompositor")
    chrome_options.add_argument("--silent")
    chrome_options.add_argument("--log-level=3")  # Suppress logs
    
    # Use persistent profile
    profile_path = r"C:\num\chrome_profile"
    if os.path.exists(profile_path):
        chrome_options.add_argument(f"--user-data-dir={profile_path}")
    
    # Disable automation detection
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, \"webdriver\", {get: () => undefined})")
        print(" Silent Chrome driver created")
        return driver
    except Exception as e:
        print(f" Error creating silent driver: {e}")
        return None

def silent_whatsapp_init(driver):
    """Initialize WhatsApp without showing browser"""
    try:
        print(" Loading WhatsApp Web silently...")
        driver.get("https://web.whatsapp.com")
        
        # Wait for page to load
        time.sleep(10)
        
        # Check if logged in by looking for chat list
        try:
            driver.find_element(By.CSS_SELECTOR, "[data-testid=chat-list]")
            print(" Already logged in!")
            return True
        except:
            # Check for QR code
            try:
                driver.find_element(By.CSS_SELECTOR, "[data-testid=qr-code]")
                print(" QR code required - cannot proceed in headless mode")
                return False
            except:
                print("  Unknown state, assuming logged in")
                return True
                
    except Exception as e:
        print(f" Error initializing WhatsApp: {e}")
        return False

def check_registration_silent(phone_number, driver):
    """Check registration silently without browser dialogs"""
    try:
        clean_number = phone_number.replace("+", "").replace("-", "").replace(" ", "")
        print(f" Silently checking: {phone_number}")
        
        # Navigate to WhatsApp chat URL
        chat_url = f"https://web.whatsapp.com/send?phone={clean_number}"
        driver.get(chat_url)
        time.sleep(8)
        
        # Check current state
        current_url = driver.current_url
        page_source = driver.page_source.lower()
        
        # Method 1: Look for chat interface
        try:
            chat_selectors = [
                "[role=textbox]",
                "[data-testid=compose-box-input]",
                "[data-testid=conversation-header]",
                "._13NKt"
            ]
            
            for selector in chat_selectors:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    print(" REGISTERED - Chat interface found")
                    return True
        except:
            pass
        
        # Method 2: Check for error messages
        error_indicators = [
            "invalid phone",
            "not registered", 
            "número inválido",
            "phone number shared via url is invalid"
        ]
        
        for error in error_indicators:
            if error in page_source:
                print(" NOT REGISTERED - Error detected")
                return False
        
        # Method 3: URL analysis
        if "send?phone=" in current_url and "chat" not in current_url:
            # Still on send page, check if it should redirect
            time.sleep(3)
            if driver.current_url == current_url:
                print(" NOT REGISTERED - No chat redirect")
                return False
        
        print(" REGISTERED - Accessible")
        return True
        
    except Exception as e:
        print(f" Error in silent check: {e}")
        return False

def test_silent_checker():
    """Test the silent checker"""
    numbers_to_test = [
        "+919585914267",  # Your number
        "+1234567890",    # Fake number for testing
    ]
    
    print(" Silent WhatsApp Registration Checker")
    print("=" * 45)
    print(" Running completely in background")
    print(" No browser windows will appear")
    print()
    
    # Create silent driver
    driver = create_silent_driver()
    if not driver:
        print(" Failed to create silent driver")
        return
    
    try:
        # Initialize WhatsApp
        if not silent_whatsapp_init(driver):
            print(" Cannot proceed without QR login")
            print(" Run regular checker first to login, then use silent mode")
            return
        
        print(" WhatsApp initialized silently")
        print()
        
        # Test each number
        results = []
        for i, number in enumerate(numbers_to_test, 1):
            print(f"[{i}/{len(numbers_to_test)}] Testing: {number}")
            
            result = check_registration_silent(number, driver)
            results.append({
                "number": number,
                "registered": result
            })
            
            status = " REGISTERED" if result else " NOT REGISTERED"
            print(f"   Result: {status}")
            print()
            
            time.sleep(2)  # Small delay between checks
        
        # Summary
        print(" SILENT CHECK SUMMARY:")
        print("=" * 25)
        for result in results:
            status = " REG" if result["registered"] else " NOT REG"
           
        
        registered_count = sum(1 for r in results if r["registered"])
        print(f"\n   Total: {len(results)} | Registered: {registered_count}")
        
    except Exception as e:
        print(f" Silent test failed: {e}")
    
    finally:
        print("\n Closing silent browser...")
        driver.quit()
        print(" Silent check completed!")

def quick_silent_check(phone_number):
    """Quick single number check silently"""
    print(f" Quick Silent Check: {phone_number}")
    
    driver = create_silent_driver()
    if not driver:
        return False
    
    try:
        if silent_whatsapp_init(driver):
            result = check_registration_silent(phone_number, driver)
            status = "REGISTERED" if result else "NOT REGISTERED"
            print(f" Result: {phone_number} is {status}")
            return result
        else:
            print(" Cannot initialize WhatsApp silently")
            return False
    finally:
        driver.quit()
if __name__ == "__main__":
    # Run full test
    test_silent_checker()
    
    # Uncomment for quick single check:
    # quick_silent_check("+919585914267")
