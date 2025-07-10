from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from src.utils.config_reader import ConfigReader


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait_timeout = ConfigReader.get_wait_times()['explicit_wait']
        self.base_url = ConfigReader.get_base_url()

    def find_element(self, locator, timeout=None):
        """Find and return a visible element"""
        timeout = timeout or self.wait_timeout
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def find_elements(self, locator, timeout=None):
        """Find and return all elements that are present"""
        timeout = timeout or self.wait_timeout
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located(locator)
        )

    def click(self, locator, timeout=None):
        """Click on an element"""
        timeout = timeout or self.wait_timeout
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()

    def type_text(self, locator, text, clear_first=True, timeout=None):
        """Type text into an element"""
        timeout = timeout or self.wait_timeout
        element = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
        if clear_first:
            element.clear()
        element.send_keys(text)
        
    def navigate_to_page(self, path=""):
        """Navigate to a specific path on the site"""
        self.driver.get(f"{self.base_url}{path}")
            
    def wait_for_element_visible(self, locator, timeout=None):
        """Wait for an element to be visible"""
        timeout = timeout or self.wait_timeout
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
        
    def wait_for_element_clickable(self, locator, timeout=None):
        """Wait for an element to be clickable"""
        timeout = timeout or self.wait_timeout
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        
    def get_text(self, locator, timeout=None):
        """Get text from an element"""
        return self.find_element(locator, timeout).text
        
    def get_attribute(self, locator, attribute, timeout=None):
        """Get attribute value from an element"""
        return self.find_element(locator, timeout).get_attribute(attribute)
    
    def is_element_visible(self, locator, timeout=5):
        """Check if an element is visible"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    def is_element_present(self, locator, timeout=5):
        """Check if an element is present in the DOM"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False