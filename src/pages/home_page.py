from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException


class HomePage(BasePage):
    # Locators
    PROFILE_IMAGE = (By.XPATH, '//img[@alt="profile picture" and @class="oxd-userdropdown-img"]')
    ADMIN_NAVIGATION_BUTTON = (By.XPATH, "//span[text()='Admin']")
    SEARCH_BUTTON = (By.XPATH, "//button[@type='submit' and contains(., 'Search')]")
   
    def __init__(self, driver):
        super().__init__(driver)
    
    def click_on_admin_navigation(self):
        """Click on the Admin navigation button"""
        self.click(self.ADMIN_NAVIGATION_BUTTON)
        print("✅ Clicked Admin navigation")

    def select_dropdown(self, label: str, option_text: str):
        """Select an option from dropdown by label"""
        # Click dropdown
        dropdown_locator = (By.XPATH, 
            f"//label[text()='{label}']/ancestor::div[contains(@class, 'oxd-input-group')]//div[@tabindex='0']"
        )
        self.click(dropdown_locator)
        print(f"✅ Clicked {label} dropdown")

        # Select option from listbox
        option_locator = (By.XPATH, 
            f"//div[@role='listbox']//div[@role='option']//span[text()='{option_text}']"
        )
        self.click(option_locator)
        print(f"✅ Selected '{option_text}' from {label} dropdown")

    def type_in_employee_name(self, employee_name):
        """Type employee name and select from autocomplete"""
        # Type in employee name field
        employee_input_locator = (By.XPATH,
            "//label[text()='Employee Name']/ancestor::div[contains(@class, 'oxd-input-group')]//input[@placeholder='Type for hints...']"
        )
        self.type_text(employee_input_locator, employee_name)
        print(f"✅ Typed '{employee_name}' in Employee Name field")

        # Wait for searching to complete
        WebDriverWait(self.driver, 10).until_not(
            EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Searching...")
        )

        # Click first option from autocomplete
        first_option_locator = (By.XPATH, "//div[@role='listbox']//div[@role='option'][1]")
        self.click(first_option_locator)
        print("✅ Selected employee from autocomplete")

    def type_in_username(self, username):
        """Type username in the username field"""
        username_input_locator = (By.XPATH,
            "//label[text()='Username']/ancestor::div[contains(@class, 'oxd-input-group')]//input"
        )
        self.type_text(username_input_locator, username)
        print(f"✅ Typed username '{username}'")
    
    def click_search_button(self):
        """Click the search button"""
        self.click(self.SEARCH_BUTTON)
        print("✅ Clicked search button")

    def delete_user_by_username(self, username):
        """Delete a user by username with retry logic"""
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                # Wait for search results
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@role='row']"))
                )
                
                # Find and click delete button
                delete_button_locator = (By.XPATH, 
                    f"//div[@role='row'][.//div[contains(text(), '{username}')]]//button[.//i[contains(@class, 'bi-trash')]]"
                )
                self.click(delete_button_locator)
                print(f"✅ Clicked delete button for user: {username}")
                return
                
            except StaleElementReferenceException:
                if attempt == max_retries - 1:
                    raise
                print(f"⚠️ Retrying delete operation ({attempt + 1}/{max_retries})")
                continue
                
            except Exception as e:
                print(f"❌ Failed to delete user {username}: {str(e)}")
                raise

    def confirm_delete(self):
        """Click the delete confirmation button"""
        confirm_button_locator = (By.XPATH, "//button[contains(., 'Yes, Delete')]")
        self.click(confirm_button_locator)
        print("✅ Confirmed deletion")

    def verify_no_records_found(self):
        """Verify that 'No Records Found' message is displayed"""
        no_records_locator = (By.XPATH, "//span[text()='No Records Found']")
        
        try:
            self.wait_for_element_visible(no_records_locator, timeout=10)
            print("✅ 'No Records Found' message is displayed")
            return True
        except TimeoutException:
            print("❌ 'No Records Found' message not found")
            return False