from checker.whatsapp_checker import check_whatsapp_number
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def create_driver():
    """Create a Chrome driver with persistent profile"""
    options = Options()
    options.add_argument(r'--user-data-dir=.\chrome_profile')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--remote-debugging-port=9222')
    
    # Use webdriver-manager to automatically download and manage ChromeDriver
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def test_single_number():
    """Test a single number"""
    number = "+919943899583"  # Replace with a real number you want to check
    
    print("🚀 Starting WhatsApp number check...")
    
    driver = None
    try:
        # Create driver
        print("📱 Opening Chrome browser...")
        driver = create_driver()
        driver.get('https://web.whatsapp.com')
        
        print("📷 Please scan the QR code in the browser window that opened")
        input("After scanning QR code and WhatsApp Web loads, press Enter to continue...")
        
        # Check the number
        print(f"📞 Checking number: {number}")
        result = check_whatsapp_number(number, driver)
        print(f"✅ Result: {number} is {'registered' if result else 'NOT registered'} on WhatsApp.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        
    finally:
        if driver:
            input("\nPress Enter to close browser...")
            driver.quit()
        
    print("\nTest completed!")


if __name__ == "__main__":
    test_single_number()