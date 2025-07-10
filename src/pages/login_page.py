from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging


class LoginPage(BasePage):
    # Locators
    USER_NAME_INPUT = (By.XPATH, "//input[@placeholder='Username']")
    PASSWORD_INPUT = (By.XPATH, "//input[@placeholder='Password']")
    LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")
    DASHBOARD_ELEMENT = (By.XPATH, "//h6[text()='Dashboard']")  # OrangeHRM dashboard indicator
    ERROR_MESSAGE = (By.XPATH, "//p[contains(@class, 'alert-content-text')]")  # OrangeHRM error message

    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)
        
    def enter_username(self, username):
        """Enter username in the username input field"""
        self.logger.info(f"Entering username: {username}")
        self.type_text(self.USER_NAME_INPUT, username)
        
    def enter_password(self, password):
        """Enter password in the password input field"""
        self.logger.info("Entering password")
        self.type_text(self.PASSWORD_INPUT, password)
    
    def click_login_button(self):
        """Click the login button"""
        self.logger.info("Clicking login button")
        self.click(self.LOGIN_BUTTON)
    
    def is_login_successful(self, timeout=10):
        """Check if login was successful by looking for dashboard element"""
        self.logger.debug("Checking if login was successful")
        try:
            self.wait_for_element_visible(self.DASHBOARD_ELEMENT, timeout)
            self.logger.info("Dashboard found - login successful")
            return True
        except TimeoutException:
            self.logger.info("Dashboard not found - login failed")
            return False
    
    def get_error_message(self, timeout=5):
        """Get error message if login failed"""
        self.logger.debug("Checking for error message")
        try:
            error_element = self.wait_for_element_visible(self.ERROR_MESSAGE, timeout)
            error_text = error_element.text
            self.logger.info(f"Error message found: {error_text}")
            return error_text
        except TimeoutException:
            self.logger.info("No error message found")
            return None

    def login(self, username, password):
        """Perform complete login process"""
        self.logger.info(f"Performing login with username: {username}")
        
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
        
        # Check result and log
        if self.is_login_successful():
            self.logger.info("✅ Login successful")
            return True
        else:
            error_msg = self.get_error_message() or "Unknown error"
            self.logger.warning(f"❌ Login failed: {error_msg}")
            return False