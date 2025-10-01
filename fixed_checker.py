from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import os

def check_whatsapp_registration_compose_url(number):
    """
    Check if a phone number is registered on WhatsApp using compose URL method
    This method works for ANY number, not just non-contacts
    """
    print(f" Checking WhatsApp registration for: {number}")
    
    # Clean and format the number
    clean_number = re.sub(r'[^\d+]', '', number)
    if clean_number.startswith('+'):
        clean_number = clean_number[1:]  # Remove + for URL
    
    print(f" Cleaned number: {clean_number}")
    
    # Chrome profile path
    profile_path = r"C:\num\chrome_profile"
    
    # Chrome options
    chrome_options = Options()
    chrome_options.add_argument(f"--user-data-dir={profile_path}")
    chrome_options.add_argument("--profile-directory=Default")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument("--no-default-browser-check")
    
    try:
        print(" Starting Chrome WebDriver...")
        driver = webdriver.Chrome(options=chrome_options)
        driver.maximize_window()
        
        # Go to WhatsApp Web compose URL
        compose_url = f"https://web.whatsapp.com/send?phone={clean_number}"
        print(f" Opening compose URL: {compose_url}")
        
        driver.get(compose_url)
        time.sleep(3)
        
        # Wait for page to load completely
        wait = WebDriverWait(driver, 15)
        
        print(" Waiting for WhatsApp Web to load...")
        
        # Check for various indicators
        try:
            # Method 1: Look for error message about number not on WhatsApp
            error_selectors = [
                '[data-testid="alert-phone-number-not-on-whatsapp"]',
                '[data-testid="invalid-phone-number"]',
                'div[data-animate-alert-toast="true"]',
                'div[role="alert"]'
            ]
            
            for selector in error_selectors:
                try:
                    error_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                    error_text = error_element.text.lower()
                    print(f" Error found: {error_text}")
                    
                    if any(phrase in error_text for phrase in ['not on whatsapp', 'invalid', 'not found']):
                        print(" Number NOT registered on WhatsApp")
                        return False
                        
                except Exception:
                    continue
            
            # Method 2: Check if we reach the chat interface
            chat_selectors = [
                '[data-testid="conversation-compose-box-input"]',
                'div[contenteditable="true"][data-tab="10"]',
                '[data-testid="msg-container"]',
                'footer[data-testid="compose"]'
            ]
            
            for selector in chat_selectors:
                try:
                    chat_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                    print(f" Chat interface found: {selector}")
                    print(" Number IS registered on WhatsApp")
                    return True
                except Exception:
                    continue
            
            # Method 3: Check URL for success/failure patterns
            time.sleep(2)
            current_url = driver.current_url
            print(f" Current URL: {current_url}")
            
            if "send?phone=" in current_url and clean_number in current_url:
                # Still on compose URL might mean success
                print(" Still on compose URL - likely registered")
                return True
            
            print(" Unable to determine registration status clearly")
            return False
            
        except Exception as e:
            print(f" Error during checking: {str(e)}")
            return False
            
    except Exception as e:
        print(f" WebDriver error: {str(e)}")
        return False
        
    finally:
        try:
            driver.quit()
            print(" Browser closed")
        except:
            pass

# Test the problematic number
if __name__ == "__main__":
    test_number = "+916362945154"
    print(f"Testing number: {test_number}")
    result = check_whatsapp_registration_compose_url(test_number)
    print(f"Result: {'REGISTERED' if result else 'NOT REGISTERED'}")
