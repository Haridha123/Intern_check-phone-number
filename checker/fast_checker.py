from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

def check_whatsapp_number(number, driver=None):
    """
    Fast and accurate WhatsApp number checker
    """
    close_driver = False
    if driver is None:
        from selenium.webdriver.chrome.options import Options
        options = Options()
        options.add_argument('--headless')  # Run in background for speed
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(options=options)
        driver.get('https://web.whatsapp.com')
        close_driver = True

    try:
        wait = WebDriverWait(driver, 5)
        
        # Enter number in URL directly for faster checking
        driver.get(f'https://web.whatsapp.com/send/?phone={number.replace("+", "")}')
        time.sleep(2)  # Short wait for page load
        
        # Quick check for invalid number message
        try:
            invalid_msg = driver.find_element(By.XPATH, "//*[contains(text(), 'Phone number shared via url is invalid')]")
            if invalid_msg.is_displayed():
                return False
        except:
            pass

        # Look for the chat interface
        try:
            # If chat interface loads, number is registered
            chat_interface = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, '_3B19s')]")))
            return True
        except TimeoutException:
            # If we timeout waiting for chat interface, number is not registered
            return False
        except:
            pass

        # Final check for registration status
        try:
            status = driver.find_element(By.XPATH, "//*[contains(text(), 'Phone number is not on WhatsApp')]")
            if status.is_displayed():
                return False
        except:
            # If we can't find the "not on WhatsApp" message and we got this far, likely registered
            pass

        # Default to not registered if we're unsure
        return False

    finally:
        if close_driver:
            driver.quit()