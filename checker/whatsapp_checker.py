import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# Core logic for WhatsApp number checking using Selenium

def check_whatsapp_number(number, driver=None):
    """
    Checks if a phone number is registered on WhatsApp Web with improved accuracy.
    Args:
        number (str): Phone number in international format (e.g., +1234567890)
        driver (webdriver, optional): Selenium WebDriver instance. If None, creates a new one.
    Returns:
        bool: True if number is registered, False otherwise
    """
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    
    close_driver = False
    if driver is None:
        from selenium.webdriver.chrome.options import Options
        options = Options()
        options.add_argument('--disable-notifications')
        driver = webdriver.Chrome(options=options)
        driver.get('https://web.whatsapp.com')
        input("Scan QR code in the browser and press Enter to continue...")
        close_driver = True

    try:
        # Wait for search box to be present and clickable
        wait = WebDriverWait(driver, 10)
        search_box = wait.until(
            EC.presence_of_element_located((By.XPATH, '//div[@role="textbox"]'))
        )
        search_box.clear()
        search_box.send_keys(number)
        
        # Wait for search results to load (either results or no results message)
        time.sleep(3)  # Give WhatsApp time to search
        
        # First check: Look for "Phone number shared via url is invalid." message
        try:
            invalid_number = driver.find_element(By.XPATH, "//*[contains(text(), 'Phone number shared via url is invalid')]")
            if invalid_number.is_displayed():
                return False
        except NoSuchElementException:
            pass
            
        # Second check: Look for the explicit "not on WhatsApp" message
        try:
            not_on_wa = driver.find_element(By.XPATH, "//*[contains(text(), 'Phone number is not on WhatsApp')]")
            if not_on_wa.is_displayed():
                return False
        except NoSuchElementException:
            pass
        
        # Third check: Look for chat/message panel
        try:
            chat_panel = driver.find_element(By.XPATH, '//div[@role="listbox"]')
            if not chat_panel.is_displayed():
                return False
                
            # Look for the number in the results
            results = chat_panel.find_elements(By.XPATH, './/div[contains(@class, "copyable-text")]')
            for result in results:
                if number in result.get_attribute('innerText'):
                    return True
                    
            # If we found results but none match our number, it's not registered
            return False
            
        except NoSuchElementException:
            # No chat panel found at all
            return False
        except Exception as e:
            print(f"[DEBUG] Error checking search results: {e}")
            return False
    finally:
        if close_driver:
            driver.quit()
