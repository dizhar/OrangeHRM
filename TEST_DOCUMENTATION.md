# OrangeHRM Test Automation Framework - Test Documentation

## Table of Contents

1. [Overview](#overview)
2. [Test Architecture](#test-architecture)
3. [Test Environment Setup](#test-environment-setup)
4. [Test Execution Guide](#test-execution-guide)
5. [Test Cases Documentation](#test-cases-documentation)
6. [Page Object Model Implementation](#page-object-model-implementation)
7. [API Testing Integration](#api-testing-integration)
8. [Test Data Management](#test-data-management)
9. [Reporting and Analysis](#reporting-and-analysis)
10. [Debugging and Troubleshooting](#debugging-and-troubleshooting)
11. [Best Practices](#best-practices)
12. [Maintenance Guidelines](#maintenance-guidelines)

## Overview

### Framework Purpose

This test automation framework is designed to provide comprehensive testing capabilities for the OrangeHRM Human Resource Management system. It combines UI automation using Selenium WebDriver with API testing capabilities to ensure thorough validation of system functionality.

### Key Features

- **Hybrid Testing Approach**: Combines UI and API testing for comprehensive coverage
- **Page Object Model**: Maintainable and scalable test architecture
- **Parallel Execution**: Supports concurrent test execution for faster feedback
- **Cross-Platform Support**: Compatible with Windows, macOS, and Linux
- **Docker Integration**: Containerized execution for consistent environments
- **Rich Reporting**: Allure reports with screenshots, logs, and detailed test steps
- **Configuration Management**: Flexible configuration system for different environments

### Technology Stack

- **Python 3.8+**: Core programming language
- **Selenium WebDriver 4.31.0**: UI automation
- **pytest 8.3.5**: Testing framework
- **Allure 2.14.2**: Advanced reporting
- **Docker**: Containerization
- **Requests**: API testing

## Test Architecture

### Framework Structure

```
OrangeHRM/
├── src/
│   ├── pages/              # Page Object Models
│   ├── tests/              # Test implementations
│   ├── utils/              # Utility functions
│   └── config/             # Configuration files
├── reports/                # Test reports and artifacts
├── drivers/                # Browser drivers (auto-managed)
└── docker/                 # Docker configuration
```

### Design Patterns

1. **Page Object Model (POM)**: Encapsulates page elements and actions
2. **Factory Pattern**: WebDriver initialization and management
3. **Builder Pattern**: Test data creation and configuration
4. **Singleton Pattern**: Configuration management

### Test Layers

1. **UI Layer**: Selenium-based browser automation
2. **API Layer**: REST API testing and validation
3. **Data Layer**: Test data management and database interactions
4. **Utility Layer**: Common functions and helpers

## Test Environment Setup

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Chrome/Firefox browser
- Git version control
- Docker (optional)

### Local Setup

```bash
# Clone repository
git clone git@github.com:dizhar/OrangeHRM.git
cd OrangeHRM

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
pytest --version
```

### Docker Setup

```bash
# Build Docker image
chmod +x build_docker.sh
./build_docker.sh

# Run tests in container
docker-compose run test python -m pytest src/tests/ui/ -v
```

### Configuration

Edit `src/config/config.ini` for environment-specific settings:

```ini
[Browsers]
browser = chrome          # chrome, firefox
headless = false         # true for CI/CD

[Test]
implicit_wait = 10       # Seconds
explicit_wait = 20       # Seconds
page_load_time = 60      # Seconds
screenshot_on_failure = true

[OrangeHRM]
base_url = https://opensource-demo.orangehrmlive.com
admin_username = Admin
admin_password = admin123
default_password = TestPass123!
```

## Test Execution Guide

### Basic Execution

```bash
# Run all tests
pytest

# Run specific test file
pytest src/tests/ui/test_user_management.py

# Run with verbose output
pytest -v

# Run specific test method
pytest src/tests/ui/test_user_management.py::test_user_management_lifecycle
```

### Advanced Execution Options

```bash
# Parallel execution
pytest -n auto

# Run with timeout
pytest --timeout=300

# Run with custom markers
pytest -m "smoke"

# Run with specific browser
BROWSER=firefox pytest

# Headless execution
HEADLESS=true pytest
```

### Using Shell Scripts

```bash
# Unix/Linux/macOS
chmod +x run_tests.sh
./run_tests.sh

# Windows
run_tests.bat
```

### Docker Execution

```bash
# Run tests in Docker
docker-compose up test

# Interactive Docker session
docker run -it --rm orangehrm-test bash
```

## Test Cases Documentation

### Current Test Suite

#### User Management Lifecycle Test

**File**: `src/tests/ui/test_user_management.py`
**Function**: `test_user_management_lifecycle`

**Purpose**: Validates complete user management workflow including creation, verification, and deletion.

**Test Steps**:

1. **Login Authentication**

   - Navigate to OrangeHRM login page
   - Authenticate using admin credentials from config
   - Verify successful login

2. **API User Creation**

   - Initialize API helper with authenticated session
   - Create unique test user via API endpoint
   - Validate user creation response

3. **UI Navigation**

   - Navigate to Admin section
   - Access user management interface

4. **User Search and Verification**

   - Search for created user by username
   - Apply filters (User Role, Employee Name, Status)
   - Verify user appears in search results

5. **User Deletion**
   - Select user for deletion
   - Confirm deletion action
   - Verify user removal from system

**Expected Results**:

- User successfully created via API
- User visible in UI search results
- User successfully deleted via UI
- "No Records Found" message displayed after deletion

**Test Data**:

- Username: Auto-generated with "autotest" prefix
- User Role: Configurable via API
- Employee Name: Generated test data
- Status: Active/Inactive as specified

### Test Categories

#### Smoke Tests

- Basic login functionality
- Core navigation elements
- Critical user workflows

#### Regression Tests

- User management operations
- Data integrity validations
- Cross-browser compatibility

#### Integration Tests

- API-UI data consistency
- End-to-end workflows
- Third-party integrations

## Page Object Model Implementation

### Base Page Structure

**File**: `src/pages/base_page.py`

The BasePage class provides common functionality for all page objects:

- WebDriver management
- Common wait strategies
- Element interaction methods
- Screenshot capture
- Logging capabilities

### Page Object Guidelines

#### LoginPage Example

```python
class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.username_field = (By.NAME, "username")
        self.password_field = (By.NAME, "password")
        self.login_button = (By.XPATH, "//button[@type='submit']")

    def login(self, username, password):
        self.wait_and_type(self.username_field, username)
        self.wait_and_type(self.password_field, password)
        self.wait_and_click(self.login_button)
```

#### Best Practices for Page Objects

1. **Locator Strategy**: Use stable locators (ID > Name > CSS > XPath)
2. **Wait Strategies**: Implement explicit waits for all interactions
3. **Method Naming**: Use descriptive, action-oriented method names
4. **Error Handling**: Include proper exception handling
5. **Logging**: Add logging for debugging and maintenance

### Element Interaction Patterns

```python
# Wait and click pattern
def wait_and_click(self, locator, timeout=None):
    element = self.wait_for_element_clickable(locator, timeout)
    element.click()
    return element

# Wait and type pattern
def wait_and_type(self, locator, text, timeout=None):
    element = self.wait_for_element_visible(locator, timeout)
    element.clear()
    element.send_keys(text)
    return element
```

## API Testing Integration

### API Helper Implementation

**File**: `src/utils/api_helper.py`

The API helper provides methods for:

- Authentication token management
- User creation and management
- Data validation
- Session handling

### Hybrid Testing Approach

```python
def test_hybrid_scenario(driver):
    # Setup data via API (faster)
    api_helper = get_api_helper_with_auth(driver)
    user_data = api_helper.create_unique_user(prefix="test")

    # Verify via UI (user experience validation)
    home_page = HomePage(driver)
    home_page.search_user(user_data['username'])
    assert home_page.user_exists(user_data['username'])
```

### API Testing Benefits

1. **Speed**: API calls are faster than UI interactions
2. **Data Setup**: Efficient test data preparation
3. **Validation**: Backend data integrity verification
4. **Coverage**: Testing both UI and API layers

## Test Data Management

### Configuration-Based Data

Test data is managed through configuration files and dynamic generation:

```python
# Static configuration data
orangehrm_config = ConfigReader.get_orangehrm_config()
username = orangehrm_config['admin_username']

# Dynamic test data generation
user_data = api_helper.create_unique_user(prefix="autotest")
```

### Data Generation Strategies

1. **Static Data**: Configuration files for stable test data
2. **Dynamic Data**: Runtime generation for unique test scenarios
3. **Parameterized Data**: pytest fixtures for data-driven testing
4. **External Data**: JSON/CSV files for complex test datasets

### Test Data Cleanup

```python
@pytest.fixture(scope="function")
def test_user(driver):
    # Setup
    api_helper = get_api_helper_with_auth(driver)
    user_data = api_helper.create_unique_user()

    yield user_data

    # Cleanup
    api_helper.delete_user(user_data['id'])
```

## Reporting and Analysis

### Allure Reporting

The framework generates comprehensive Allure reports with:

- Test execution timeline
- Step-by-step test details
- Screenshots on failure
- Environment information
- Historical trends

#### Generating Allure Reports

```bash
# Run tests with Allure
pytest --alluredir=reports/allure-results

# Serve Allure report
allure serve reports/allure-results

# Generate static report
allure generate reports/allure-results -o reports/allure-report --clean
```

#### Allure Annotations

```python
@allure.epic("User Management")
@allure.feature("Authentication")
@allure.story("User Login")
@allure.description("Test user login functionality")
def test_login(driver):
    with allure.step("Navigate to login page"):
        # Test implementation
        pass
```

### HTML Reports

Basic HTML reports are automatically generated:

- Location: `reports/report.html`
- Self-contained with embedded CSS/JS
- Test results summary
- Failure details and screenshots

### Report Serving

```bash
# Serve Allure reports (Unix/Linux/macOS)
chmod +x serve_allure_report.sh
./serve_allure_report.sh

# Windows
serve_allure_report.bat

# Access reports at http://localhost:4040
```

## Debugging and Troubleshooting

### Debug Configuration

The framework includes VSCode debug configuration in `.vscode/launch.json`:

```json
{
  "name": "Debug Current Test",
  "type": "python",
  "request": "launch",
  "module": "pytest",
  "args": ["${file}", "-v", "-s"],
  "console": "integratedTerminal"
}
```

### Common Debugging Techniques

#### 1. Interactive Debugging

```python
import pdb; pdb.set_trace()  # Add breakpoint
```

#### 2. Screenshot Capture

```python
# Automatic on failure (configured in config.ini)
screenshot_on_failure = true

# Manual screenshot
self.driver.save_screenshot("debug_screenshot.png")
```

#### 3. Browser Developer Tools

```python
# Keep browser open for inspection
driver.quit()  # Comment out this line
input("Press Enter to continue...")  # Add pause
```

#### 4. Verbose Logging

```bash
pytest -v -s --log-cli-level=DEBUG
```

### Common Issues and Solutions

#### WebDriver Issues

```bash
# Update webdriver-manager
pip install --upgrade webdriver-manager

# Manual driver download
./download_drivers.sh
```

#### Timeout Issues

```python
# Increase wait times in config.ini
explicit_wait = 30
page_load_time = 90
```

#### Element Not Found

```python
# Use better wait strategies
element = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable(locator)
)
```

#### Docker Issues

```bash
# Check platform compatibility
docker build --platform linux/amd64 -t orangehrm-test .

# View container logs
docker-compose logs test
```

## Best Practices

### Test Design Principles

1. **Independence**: Tests should not depend on each other
2. **Repeatability**: Tests should produce consistent results
3. **Clarity**: Test intent should be obvious from code
4. **Maintainability**: Easy to update when application changes
5. **Speed**: Optimize for fast execution

### Code Quality Standards

```python
# Good test structure
def test_user_creation():
    # Arrange
    test_data = generate_user_data()

    # Act
    result = create_user(test_data)

    # Assert
    assert result.success
    assert result.user_id is not None
```

### Naming Conventions

- **Test Files**: `test_*.py`
- **Test Methods**: `test_descriptive_name`
- **Page Objects**: `*Page` (e.g., `LoginPage`)
- **Utilities**: `*_helper.py` or `*_utils.py`

### Error Handling

```python
try:
    element = driver.find_element(By.ID, "element_id")
    element.click()
except TimeoutException:
    pytest.fail("Element not found within timeout period")
except ElementNotInteractableException:
    pytest.fail("Element not interactable")
```

### Performance Optimization

1. **Parallel Execution**: Use `-n auto` for pytest-xdist
2. **Selective Testing**: Use markers for test categorization
3. **API Setup**: Use API for test data preparation
4. **Browser Reuse**: Consider session reuse for related tests

## Maintenance Guidelines

### Regular Maintenance Tasks

#### Weekly

- Review test execution reports
- Update browser drivers if needed
- Check for flaky tests
- Monitor test execution times

#### Monthly

- Update dependencies
- Review and refactor page objects
- Analyze test coverage
- Update documentation

#### Quarterly

- Major framework updates
- Performance optimization review
- Test suite architecture evaluation
- Training and knowledge sharing

### Dependency Management

```bash
# Check for outdated packages
pip list --outdated

# Update specific package
pip install --upgrade selenium

# Update all packages (with caution)
pip install --upgrade -r requirements.txt
```

### Version Control Best Practices

1. **Branching Strategy**: Use feature branches for new tests
2. **Commit Messages**: Clear, descriptive commit messages
3. **Code Reviews**: Peer review for all changes
4. **Documentation**: Update docs with code changes

### Continuous Integration

```yaml
# Example GitHub Actions workflow
name: Test Automation
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.11
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest --alluredir=reports/allure-results
      - name: Publish Allure Report
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: reports/allure-report
```

### Monitoring and Alerting

- Set up notifications for test failures
- Monitor test execution trends
- Track test coverage metrics
- Alert on performance degradation

## Conclusion

This test automation framework provides a robust foundation for testing the OrangeHRM system. By following the guidelines and best practices outlined in this documentation, teams can maintain high-quality, reliable automated tests that provide valuable feedback on system functionality.

For additional support or questions, refer to the project repository or contact the test automation team.

---

**Document Version**: 1.0  
**Last Updated**: January 2025  
**Maintained By**: Test Automation Team
