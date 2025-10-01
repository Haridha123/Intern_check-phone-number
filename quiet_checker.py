from whatsapp.selenium_checker import create_persistent_driver, initialize_whatsapp_session, check_whatsapp_number
import time

def test_quiet_registration():
    print(" Quiet Registration Check")
    print("=" * 30)
    print(" Using existing working functions")
    print(" Minimal dialog interaction")
    print()
    
    driver = create_persistent_driver()
    
    try:
        print(" Initializing session...")
        if not initialize_whatsapp_session(driver):
            print(" Failed to initialize")
            return
        
        print(" Session ready!")
        
        test_number = "+919585914267"
        print(f" Testing: {test_number}")
        
        # Contact check using existing method
        result = check_whatsapp_number(test_number, driver)
        
        print()
        print(" CONTACT CHECK RESULT:")
        status = "IN YOUR CONTACTS" if result else "NOT IN YOUR CONTACTS"
        print(f" {test_number}: {status}")
        
        # Registration check via URL
        print()
        print(" Testing Registration via URL...")
        
        clean_number = test_number.replace("+", "").replace("-", "").replace(" ", "")
        chat_url = f"https://web.whatsapp.com/send?phone={clean_number}"
        
        driver.get(chat_url)
        time.sleep(8)
        
        current_url = driver.current_url
        print(f" Current URL: {current_url[:60]}...")
        
        # Check if chat is accessible
        if "chat" in current_url or ("send?phone=" not in current_url and "web.whatsapp.com" in current_url):
            print(" REGISTERED - Chat accessible")
            reg_status = True
        else:
            print(" NOT REGISTERED - No chat access")
            reg_status = False
        
        print()
        print(" SUMMARY:")
        print("=" * 15)
        print(f" Number: {test_number}")
        contact_status = "Yes" if result else "No"
        register_status = "Yes" if reg_status else "No"
        print(f" In Contacts: {contact_status}")
        print(f" Registered: {register_status}")
        
    except Exception as e:
        print(f" Error: {e}")
    
    finally:
        input("\n  Press Enter to close...")
        driver.quit()

if __name__ == "__main__":
    test_quiet_registration()
