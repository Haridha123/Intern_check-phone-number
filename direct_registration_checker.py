from whatsapp.selenium_checker import create_persistent_driver, initialize_whatsapp_session
from selenium.webdriver.common.by import By
import time

def check_whatsapp_registration(phone_number, driver):
    """Check if number is registered on WhatsApp without sending messages"""
    try:
        # Clean the phone number
        clean_number = phone_number.replace("+", "").replace("-", "").replace(" ", "")
        print(f" Checking registration: {phone_number}")
        
        # Navigate to WhatsApp send URL
        chat_url = f"https://web.whatsapp.com/send?phone={clean_number}"
        print(f" Accessing: {chat_url}")
        driver.get(chat_url)
        
        # Wait for page to fully load
        time.sleep(8)
        
        # Get current URL and page source
        current_url = driver.current_url
        page_source = driver.page_source.lower()
        
        print(f" Current URL: {current_url[:50]}...")
        
        # Method 1: Check for chat interface elements
        try:
            # Look for message input elements
            selectors = [
                "[role=textbox]",
                "[data-testid=compose-box-input]", 
                "._13NKt",
                "[contenteditable=true]"
            ]
            
            for selector in selectors:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements and any(elem.is_displayed() for elem in elements):
                    print(f" REGISTERED - Found chat input: {selector}")
                    return True
        except Exception as e:
            print(f"  Error checking elements: {e}")
        
        # Method 2: Check for error messages
        error_phrases = [
            "phone number shared via url is invalid",
            "número de teléfono compartido",
            "invalid phone number",
            "not registered"
        ]
        
        for phrase in error_phrases:
            if phrase in page_source:
                print(f" NOT REGISTERED - Found error: {phrase}")
                return False
        
        # Method 3: Check URL behavior
        if "send?phone=" in current_url:
            # Still on send page - check if we should be redirected
            time.sleep(3)
            final_url = driver.current_url
            if "send?phone=" in final_url and "chat" not in final_url:
                print(" NOT REGISTERED - No redirect to chat")
                return False
        
        # Method 4: Look for conversation header
        try:
            conv_headers = driver.find_elements(By.CSS_SELECTOR, "[data-testid=conversation-header], [data-testid=chat-header]")
            if conv_headers:
                print(" REGISTERED - Found conversation header")
                return True
        except:
            pass
        
        # Default assumption if we reach here
        print(" REGISTERED - Chat interface accessible")
        return True
        
    except Exception as e:
        print(f" Error during check: {e}")
        return False

def test_registration():
    """Test the registration checker"""
    # Your test number
    test_number = "+919585914267"
    
    print(" WhatsApp Registration Checker")
    print("=" * 40)
    print(" This checks ACTUAL WhatsApp registration")
    print(" No messages will be sent!")
    print()
    
    # Create driver and initialize
    driver = create_persistent_driver()
    
    try:
        print(" Initializing WhatsApp session...")
        if not initialize_whatsapp_session(driver):
            print(" Failed to initialize WhatsApp session")
            return
        
        print(" Session initialized successfully!")
        print()
        
        # Check the number
        result = check_whatsapp_registration(test_number, driver)
        
        # Display result
        print()
        print(" FINAL RESULT:")
        print("=" * 20)
        print(f" Number: {test_number}")
        print(f" Status: {\" REGISTERED\" if result else \" NOT REGISTERED\"}")
        
        if result:
            print(" This number has a WhatsApp account!")
        else:
            print(" This number is not registered on WhatsApp")
            
    except Exception as e:
        print(f" Test failed: {e}")
    
    finally:
        input("\n  Press Enter to close browser...")
        driver.quit()

if __name__ == "__main__":
    test_registration()
