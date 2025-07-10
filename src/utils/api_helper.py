import json
import time
import requests
import allure
from typing import Dict, Any, Optional
from src.utils.config_reader import ConfigReader


class OrangeHRMApiHelper:
    """Helper class for OrangeHRM API operations"""
    
    def __init__(self, base_url: Optional[str] = None):
        self.config = ConfigReader.get_orangehrm_config()
        self.base_url = base_url or self.config['base_url']
        
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
    
    def set_auth_cookie(self, cookie_value: str):
        """Set authentication cookie for API requests"""
        self.session.cookies.set('orangehrm', cookie_value)
    
    def create_user(self, username: str, password: Optional[str] = None, 
                   user_role_id: int = 1, emp_number: int = 7, 
                   status: bool = True) -> Dict[str, Any]:
        """Create a new system user"""
        password = password or self.config['default_password']
        url = f"{self.base_url}/web/index.php/api/v2/admin/users"
        
        payload = {
            "username": username,
            "password": password,
            "status": status,
            "userRoleId": user_role_id,
            "empNumber": emp_number
        }
        
        response = self.session.post(url, json=payload)
        self._log_response(response, "Create User")
        
        if response.status_code != 200:
            raise Exception(f"Failed to create user '{username}'. Status: {response.status_code}")
        
        response_data = response.json()
        user_data = self._extract_user_data(response_data)
        
        allure.attach(json.dumps(user_data, indent=2), "Created User Data", allure.attachment_type.JSON)
        return user_data
    
    def create_unique_user(self, prefix: str = "autotest", **kwargs) -> Dict[str, Any]:
        """Create a user with auto-generated unique username"""
        unique_username = f"{prefix}_{int(time.time())}"
        return self.create_user(username=unique_username, **kwargs)
    
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user information by username"""
        url = f"{self.base_url}/web/index.php/api/v2/admin/users"
        response = self.session.get(url, params={"username": username})
        
        if response.status_code == 200:
            data = response.json()
            if data.get('data') and len(data['data']) > 0:
                return data['data'][0]
        return None
    
    def delete_user_by_id(self, user_id: int) -> bool:
        """Delete user by ID via API"""
        url = f"{self.base_url}/web/index.php/api/v2/admin/users"
        response = self.session.delete(url, json={"ids": [user_id]})
        
        self._log_response(response, "Delete User")
        return response.status_code == 200
    
    def _extract_user_data(self, response_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract and format user data from API response"""
        data = response_data['data']
        return {
            'username': data['userName'],
            'user_role': data['userRole']['name'],
            'employee_name': self._format_employee_name(data['employee']),
            'status': 'Enabled' if data['status'] else 'Disabled',
            'raw_response': response_data
        }
    
    def _format_employee_name(self, employee_data: Dict[str, Any]) -> str:
        """Format employee name from API response"""
        first_name = employee_data.get('firstName', '') or ''
        middle_name = employee_data.get('middleName', '') or ''
        last_name = employee_data.get('lastName', '') or ''
        
        full_name = f"{first_name} {middle_name} {last_name}".strip()
        return ' '.join(full_name.split())
    
    def _log_response(self, response: requests.Response, operation: str):
        """Log API response for debugging"""
        allure.attach(
            f"{operation} - Status: {response.status_code}", 
            "API Response Status", 
            allure.attachment_type.TEXT
        )
        allure.attach(response.text, f"{operation} Response", allure.attachment_type.JSON)


def get_api_helper_with_auth(driver) -> OrangeHRMApiHelper:
    """Get API helper with authentication from browser session"""
    api_helper = OrangeHRMApiHelper()
    
    orangehrm_cookie = driver.get_cookie("orangehrm")
    if not orangehrm_cookie:
        raise Exception("No orangehrm cookie found in browser session")
    
    api_helper.set_auth_cookie(orangehrm_cookie['value'])
    return api_helper