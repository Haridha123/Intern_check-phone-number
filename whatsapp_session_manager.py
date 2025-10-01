#!/usr/bin/env python3
"""
WhatsApp Session Manager
Manages persistent WhatsApp Web sessions to avoid QR scanning every time
"""

import os
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class WhatsAppSessionManager:
    def __init__(self, session_name="default"):
        self.base_dir = r"C:\num\whatsapp_sessions"
        self.session_name = session_name
        self.session_dir = os.path.join(self.base_dir, session_name)
        self.ensure_directories()
    
    def ensure_directories(self):
        """Create session directories if they don't exist"""
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)
        if not os.path.exists(self.session_dir):
            os.makedirs(self.session_dir)
    
    def create_driver(self, headless=False):
        """Create Chrome driver with persistent session"""
        options = Options()
        
        # Use session-specific profile
        options.add_argument(f"--user-data-dir={self.session_dir}")
        options.add_argument("--profile-directory=Profile")
        
        # Chrome options for stability
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-plugins")
        options.add_argument("--disable-images")
        options.add_argument("--disable-javascript")
        options.add_argument("--window-size=1200,800")
        
        if headless:
            options.add_argument("--headless")
        
        # Anti-detection options
        options.add_experimental_option("useAutomationExtension", False)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_argument("--disable-blink-features=AutomationControlled")
        
        try:
            driver = webdriver.Chrome(options=options)
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            return driver
        except Exception as e:
            print(f"Error creating driver: {e}")
            return None
    
    def save_session(self, driver):
        """Save current session data"""
        try:
            # Session is automatically saved by Chrome profile
            print(f"Session saved for {self.session_name}")
            return True
        except Exception as e:
            print(f"Error saving session: {e}")
            return False
    
    def session_exists(self):
        """Check if session data exists"""
        profile_path = os.path.join(self.session_dir, "Profile")
        return os.path.exists(profile_path) and len(os.listdir(profile_path)) > 0
    
    def delete_session(self):
        """Delete session data"""
        try:
            if os.path.exists(self.session_dir):
                shutil.rmtree(self.session_dir)
                print(f"Session {self.session_name} deleted")
            return True
        except Exception as e:
            print(f"Error deleting session: {e}")
            return False
