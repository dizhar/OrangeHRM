# OrangeHRM Test Automation Framework

A comprehensive Python-based test automation framework using Selenium and pytest for UI testing of the OrangeHRM system. This framework implements the Page Object Model design pattern for maintainable and scalable test automation, with comprehensive Allure reporting and Docker support.

## Features

- **Page Object Model (POM)** design pattern for maintainable test code
- **Selenium WebDriver** for UI automation
- **Allure reporting** with detailed test results and screenshots
- **Docker containerization** for consistent test execution
- **API testing capabilities** for hybrid test scenarios
- **Parallel test execution** support
- **Cross-platform compatibility** (Windows, macOS, Linux)
- **Automatic driver management** with webdriver-manager
- **Configurable test environments** via configuration files

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Chrome or Firefox browser
- Docker (optional, for containerized execution)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/dizhar/OrangeHRM.git
   cd orangeHRM
   ```

2. Create and activate a virtual environment:

   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Download browser drivers (automatic with webdriver-manager):

   ```bash
   # On macOS/Linux
   chmod +x download_drivers.sh
   ./download_drivers.sh

   # On Windows - drivers are managed automatically by webdriver-manager
   ```

5. Install Allure (for enhanced reports):

   ```bash
   # On Windows (using Scoop)
   scoop install allure

   # On macOS
   brew install allure

   # On Linux
   sudo apt-add-repository ppa:qameta/allure
   sudo apt-get update
   sudo apt-get install allure
   ```

## Running Tests

### Local Execution

#### Basic Test Execution

```bash
# Run all tests
pytest

# Run specific test file
pytest src/tests/ui/test_user_management.py

# Run with verbose output
pytest -v

# Run tests in parallel
pytest -n auto

# Run with timeout
pytest --timeout=300
```

#### Using Provided Scripts

```bash
# Run tests and generate reports (macOS/Linux)
chmod +x run_tests.sh
./run_tests.sh

# Run tests and generate reports (Windows)
run_tests.bat

# Serve Allure report via HTTP server
chmod +x serve_allure_report.sh
./serve_allure_report.sh
```

### Docker Execution

#### Build and Run Tests

```bash
# Build Docker image
chmod +x build_docker.sh
./build_docker.sh

# Run tests using Docker Compose
docker-compose run test python -m pytest src/tests/ui/ -v -s

# Run tests and serve Allure reports
docker-compose up
```

#### Access Reports

- Allure reports: http://localhost:4040
- HTML reports: `reports/report.html`

## Project Structure

```
OrangeHRM/
│
├── src/                         # Source code directory
│   ├── pages/                   # Page Object Models
│   │   ├── __init__.py
│   │   ├── base_page.py         # Base page with common methods
│   │   ├── home_page.py         # OrangeHRM home/admin page
│   │   └── login_page.py        # OrangeHRM login page
│   │
│   ├── tests/                   # Test directory
│   │   ├── __init__.py
│   │   └── ui/                  # UI tests
│   │       ├── __init__.py
│   │       └── test_user_management.py  # User management tests
│   │
│   ├── utils/                   # Utility functions and helpers
│   │   ├── __init__.py
│   │   ├── api_helper.py        # API testing utilities
│   │   ├── config_reader.py     # Configuration reader
│   │   └── driver_factory.py    # WebDriver initialization
│   │
│   ├── config/                  # Configuration files
│   │   └── config.ini           # Main configuration
│   │
│   └── __init__.py
│
├── drivers/                     # Browser drivers (auto-downloaded)
│   ├── chromedriver
│   └── geckodriver
│
├── reports/                     # Test reports and artifacts
│   ├── allure-results/          # Allure raw results
│   ├── screenshots/             # Failure screenshots
│   ├── logs/                    # Test execution logs
│   └── report.html              # HTML test report
│
├── .vscode/                     # VSCode configuration
│   └── launch.json              # Debug configuration
│
├── conftest.py                  # Pytest fixtures and configuration
├── pytest.ini                  # Pytest configuration
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Docker configuration
├── docker-compose.yml           # Docker Compose configuration
├── build_docker.sh              # Docker build script
├── download_drivers.sh          # Driver download script
├── run_tests.sh                 # Test execution script (Unix)
├── run_tests.bat                # Test execution script (Windows)
├── serve_allure_report.sh       # Allure report server script
├── serve_allure_report.bat      # Allure report server script (Windows)
└── README.md                    # This file
```

## Configuration

### Main Configuration (src/config/config.ini)

The configuration file contains settings for:

```ini
[Browsers]
browser = chrome                 # Browser type (chrome/firefox)
headless = false                # Headless mode (true/false)

[Test]
implicit_wait = 10              # Implicit wait timeout
explicit_wait = 20              # Explicit wait timeout
page_load_time = 60             # Page load timeout
screenshot_on_failure = true    # Screenshot on test failure

[OrangeHRM]
base_url = https://opensource-demo.orangehrmlive.com
admin_username = Admin
admin_password = admin123
default_password = TestPass123!
```

### Environment Variables

You can override configuration using environment variables:

- `HEADLESS=true` - Run in headless mode
- `ENVIRONMENT=prod` - Set environment
- `CI=true` - CI/CD mode

## Test Reports

### HTML Reports

Basic HTML reports are automatically generated in the `reports/` directory.

### Allure Reports

Enhanced Allure reports provide detailed test execution information:

```bash
# Generate and serve Allure report
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

**Note:** When opening Allure reports directly from the file system, browsers may block loading due to CORS restrictions. Always use `allure serve` or the provided scripts.

## Test Development

### Adding New Tests

1. Create test files in `src/tests/ui/`
2. Follow the Page Object Model pattern
3. Use Allure annotations for better reporting:

```python
import allure
from src.pages.login_page import LoginPage

@allure.epic("User Management")
@allure.feature("Authentication")
@allure.story("User Login")
def test_user_login(driver):
    with allure.step("Navigate to login page"):
        login_page = LoginPage(driver)
        login_page.navigate_to_page()

    with allure.step("Perform login"):
        login_page.login("username", "password")
```

### Page Object Model Guidelines

1. Inherit from `BasePage` for common functionality
2. Use descriptive method names
3. Implement proper wait strategies
4. Add logging and error handling

### API Testing Integration

The framework supports hybrid UI/API testing:

```python
from src.utils.api_helper import get_api_helper_with_auth

def test_hybrid_scenario(driver):
    # Setup via API
    api_helper = get_api_helper_with_auth(driver)
    user_data = api_helper.create_unique_user(prefix="test")

    # Verify via UI
    # ... UI verification steps
```

## Debugging

### Local Debugging

```python
# Add breakpoint in code
import pdb; pdb.set_trace()
```

### VSCode Debugging

Use the provided `.vscode/launch.json` configuration for debugging tests directly in VSCode.

### Docker Debugging

```bash
# Run container interactively
docker run -it --rm orangehrm-test bash

# View logs
docker-compose logs test
```

## CI/CD Integration

### GitHub Actions Example

```yaml
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
      - name: Generate Allure report
        run: allure generate reports/allure-results -o reports/allure-report --clean
```

### Jenkins Pipeline

```groovy
pipeline {
    agent any
    stages {
        stage('Setup') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Test') {
            steps {
                sh 'pytest --alluredir=reports/allure-results'
            }
        }
        stage('Report') {
            steps {
                allure([
                    includeProperties: false,
                    jdk: '',
                    properties: [],
                    reportBuildPolicy: 'ALWAYS',
                    results: [[path: 'reports/allure-results']]
                ])
            }
        }
    }
}
```

## Dependencies

### Core Testing Packages

- `pytest==8.3.5` - Testing framework
- `pytest-html==4.1.1` - HTML reporting
- `allure-pytest==2.14.2` - Allure integration
- `pytest-xdist==3.6.0` - Parallel execution
- `pytest-check==2.2.0` - Soft assertions
- `pytest-timeout>=2.1.0` - Test timeout handling

### Selenium & WebDriver

- `selenium==4.31.0` - Web automation
- `webdriver-manager==3.8.6` - Automatic driver management

### API Testing

- `requests==2.32.3` - HTTP requests

### Utilities

- `python-dotenv==1.0.0` - Environment variables
- `configparser==6.0.0` - Configuration management

## Troubleshooting

### Common Issues

1. **Driver Issues**: Ensure webdriver-manager is properly installed
2. **Timeout Errors**: Adjust wait times in configuration
3. **Docker Issues**: Check platform compatibility (ARM64 vs AMD64)
4. **Report Access**: Use `allure serve` instead of opening files directly

### Support

For issues and questions:

1. Check the logs in `reports/logs/`
2. Review screenshots in `reports/screenshots/`
3. Examine Allure reports for detailed test execution information

## Contributing

1. Follow the existing code structure and patterns
2. Add appropriate tests for new functionality
3. Update documentation as needed
4. Ensure all tests pass before submitting changes
