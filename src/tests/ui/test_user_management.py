import allure
from src.pages.home_page import HomePage
from src.pages.login_page import LoginPage
from src.utils.api_helper import get_api_helper_with_auth
from src.utils.config_reader import ConfigReader



@allure.epic("OrangeHRM User Management")
@allure.feature("User Administration")
@allure.story("Create and Delete System Users")
@allure.description("""
This test verifies the user management functionality:
1. Login to OrangeHRM system
2. Create a new system user via API
3. Verify the user was created successfully
4. Delete the created user via UI
5. Verify the user was deleted successfully
""")


def test_user_management_lifecycle(driver):
    with allure.step("Initialize page objects"):
        login_page = LoginPage(driver)
        home_page = HomePage(driver)
        
    with allure.step("Login to OrangeHRM system"):
        login_page.navigate_to_page()
        
        # Use config for login credentials
        orangehrm_config = ConfigReader.get_orangehrm_config()
        login_page.login(orangehrm_config['admin_username'], orangehrm_config['admin_password'])
        
    with allure.step("Setup API helper with authentication"):
        api_helper = get_api_helper_with_auth(driver)
        
    with allure.step("Create a new system user via API"):
        # API helper now uses config automatically
        user_data = api_helper.create_unique_user(prefix="autotest")
        print(f"✅ User created successfully: {user_data['username']}")
        
        
    with allure.step("Navigate to Admin section for user deletion"):
        home_page.navigate_to_page()
        home_page.click_on_admin_navigation()
        
    with allure.step("Search for the created user"):
        home_page.type_in_username(user_data['username'])
        home_page.select_dropdown('User Role', user_data['user_role'])
        home_page.type_in_employee_name(user_data['employee_name'])
        home_page.select_dropdown('Status', user_data['status'])
        home_page.click_search_button()
        
    with allure.step("Delete the user via UI"):
        home_page.delete_user_by_username(user_data['username'])
        home_page.confirm_delete()
        
    with allure.step("Verify user deletion"):
        home_page.click_search_button()
        assert home_page.verify_no_records_found() == True, "User was not deleted"
        print(f"✅ User deletion completed: {user_data['username']}")