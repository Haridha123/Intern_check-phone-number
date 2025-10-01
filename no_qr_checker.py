from whatsapp.selenium_checker import check_whatsapp_number, create_persistent_driver, initialize_whatsapp_session

def test_single_number():
    """Test a single number with persistent session"""
    number = "+919585914263"  # Replace with a real number you want to check
    
    print("🚀 Starting WhatsApp number check with persistent session...")
    
    # Create persistent driver
    driver = create_persistent_driver()
    
    try:
        # Initialize session (will use saved login if available)
        if not initialize_whatsapp_session(driver):
            print("❌ Failed to initialize WhatsApp session")
            return
        
        # Check the number
        print(f"📞 Checking number: {number}")
        result = check_whatsapp_number(number, driver)
        print(f"✅ Result: {number} is {'registered' if result else 'NOT registered'} on WhatsApp.")
        
    finally:
        input("\nPress Enter to close browser...")
        driver.quit()

if __name__ == "__main__":
    test_single_number()