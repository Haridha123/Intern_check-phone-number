#!/usr/bin/env python3
"""
Enhanced WhatsApp Checker with Session Management
No QR scanning needed after first setup!
"""

from whatsapp_session_manager import WhatsAppSessionManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

class WhatsAppChecker:
    def __init__(self, session_name="whatsapp_checker"):
        self.session_manager = WhatsAppSessionManager(session_name)
        self.driver = None
        self.is_logged_in = False
    
    def start_session(self):
        """Start WhatsApp session"""
        print(f"[INFO] Starting WhatsApp session...")
        
        # Create driver
        self.driver = self.session_manager.create_driver()
        if not self.driver:
            print("[ERROR] Failed to create driver")
            return False
        
        # Initialize WhatsApp
        if not self._initialize_whatsapp():
            print("[ERROR] Failed to initialize WhatsApp")
            return False
        
        self.is_logged_in = True
        print("[SUCCESS] WhatsApp session ready!")
        return True
    
    def _initialize_whatsapp(self):
        """Initialize WhatsApp Web"""
        try:
            print("[DEBUG] Opening WhatsApp Web...")
            self.driver.get("https://web.whatsapp.com")
            
            wait = WebDriverWait(self.driver, 45)
            
            # Check if already logged in
            try:
                chat_list = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="chat-list"]')
                print("[DEBUG] Already logged in!")
                return True
            except NoSuchElementException:
                pass
            
            # Wait for QR scan
            print("[INFO] Please scan QR code...")
            
            # Wait for login success
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="chat-list"]')))
            print("[DEBUG] Login successful!")
            
            # Save session
            self.session_manager.save_session(self.driver)
            return True
            
        except TimeoutException:
            print("[ERROR] Login timeout")
            return False
        except Exception as e:
            print(f"[ERROR] Initialization failed: {e}")
            return False
    
    def check_number(self, phone_number):
        """Check if phone number is registered on WhatsApp"""
        if not self.is_logged_in:
            print("[ERROR] Session not started")
            return False
        
        try:
            print(f"[INFO] Checking {phone_number}...")
            
            # Navigate to new contact
            return self._check_registration_status(phone_number)
            
        except Exception as e:
            print(f"[ERROR] Failed to check {phone_number}: {e}")
            return False
    
    def _check_registration_status(self, number):
        """Core registration checking logic"""
        try:
            wait = WebDriverWait(self.driver, 15)
            
            # Open new chat menu
            new_chat = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="new-chat-plus"]')))
            new_chat.click()
            time.sleep(2)
            
            # Click new contact
            new_contact = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="new-contact"]')))
            new_contact.click()
            time.sleep(2)
            
            # Enter phone number
            phone_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="tel"]')))
            phone_input.clear()
            phone_input.send_keys(number)
            time.sleep(3)
            
            # Analyze result
            result = self._analyze_registration_result()
            
            # Close dialog
            self._close_dialogs()
            
            return result
            
        except Exception as e:
            print(f"[ERROR] Registration check failed: {e}")
            self._close_dialogs()
            return False
    
    def _analyze_registration_result(self):
        """Analyze WhatsApp registration status"""
        try:
            # Check for error messages
            error_messages = [
                "Phone number shared via url is invalid",
                "doesn't have WhatsApp",
                "not on WhatsApp",
                "This contact does not have WhatsApp"
            ]
            
            page_source = self.driver.page_source.lower()
            
            for error_msg in error_messages:
                if error_msg.lower() in page_source:
                    print(f"[DEBUG] NOT REGISTERED - Error: {error_msg}")
                    return False
            
            # Check next button status
            try:
                next_button = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="forward-btn"]')
                if next_button and next_button.is_enabled():
                    print("[DEBUG] REGISTERED - Next button enabled")
                    return True
                else:
                    print("[DEBUG] NOT REGISTERED - Next button disabled")
                    return False
            except NoSuchElementException:
                print("[DEBUG] NOT REGISTERED - No next button")
                return False
                
        except Exception as e:
            print(f"[ERROR] Analysis failed: {e}")
            return False
    
    def _close_dialogs(self):
        """Close any open dialogs"""
        try:
            close_buttons = [
                '[data-testid="x"]',
                '[data-testid="back"]',
                '[aria-label="Close"]',
                '[aria-label="Back"]'
            ]
            
            for selector in close_buttons:
                try:
                    button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if button.is_displayed():
                        button.click()
                        time.sleep(1)
                        break
                except NoSuchElementException:
                    continue
        except Exception:
            pass
    
    def check_multiple_numbers(self, numbers):
        """Check multiple phone numbers"""
        results = {}
        
        if not self.is_logged_in:
            print("[ERROR] Session not started")
            return results
        
        for number in numbers:
            try:
                result = self.check_number(number)
                results[number] = result
                print(f"[RESULT] {number}: {'REGISTERED' if result else 'NOT REGISTERED'}")
                time.sleep(3)  # Delay between checks
            except Exception as e:
                print(f"[ERROR] Failed to check {number}: {e}")
                results[number] = False
        
        return results
    
    def close_session(self):
        """Close WhatsApp session"""
        try:
            if self.driver:
                self.session_manager.save_session(self.driver)
                self.driver.quit()
                print("[INFO] Session closed")
        except Exception as e:
            print(f"[ERROR] Error closing session: {e}")

# Convenience functions
def check_single_number(phone_number, session_name="default"):
    """Quick function to check a single number"""
    checker = WhatsAppChecker(session_name)
    
    if not checker.start_session():
        return False
    
    try:
        result = checker.check_number(phone_number)
        return result
    finally:
        checker.close_session()

def check_multiple_numbers(phone_numbers, session_name="default"):
    """Quick function to check multiple numbers"""
    checker = WhatsAppChecker(session_name)
    
    if not checker.start_session():
        return {}
    
    try:
        results = checker.check_multiple_numbers(phone_numbers)
        return results
    finally:
        checker.close_session()

if __name__ == "__main__":
    # Example usage
    test_number = "+1234567890"
    result = check_single_number(test_number)
    print(f"Final result for {test_number}: {'REGISTERED' if result else 'NOT REGISTERED'}")
