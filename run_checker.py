from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from checker.whatsapp_checker import check_whatsapp_number

def main():
    # Setup Chrome options
    options = Options()
    options.add_argument("--start-maximized")  # Start maximized
    options.add_argument("--disable-notifications")  # Disable notifications
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    print("🚀 Starting WhatsApp number checker...")
    
    # Initialize the Chrome WebDriver
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        print("✅ Browser started successfully")
        
        # Go to WhatsApp Web
        driver.get("https://web.whatsapp.com")
        print("\n📱 Please scan the QR code in the browser window")
        input("\nAfter scanning the QR code and WhatsApp Web loads, press Enter to continue...")
        
        while True:
            # Get number from user
            number = input("\nEnter the phone number to check (or 'exit' to quit): ")
            if number.lower() == 'exit':
                break
                
            # Clean the number
            number = number.strip()
            if not number.startswith('+'):
                number = '+' + number
                
            print(f"\n🔍 Checking number: {number}")
            try:
                result = check_whatsapp_number(number, driver)
                status = "✅ REGISTERED" if result else "❌ NOT REGISTERED"
                print(f"\n{status} on WhatsApp: {number}")
            except Exception as e:
                print(f"\n⚠️ Error checking number: {e}")
                
            print("\n" + "-"*50)
            
    except Exception as e:
        print(f"\n❌ Error starting browser: {e}")
    
    finally:
        input("\nPress Enter to close the browser...")
        try:
            driver.quit()
        except:
            pass
        print("\n👋 Goodbye!")

if __name__ == "__main__":
    main()