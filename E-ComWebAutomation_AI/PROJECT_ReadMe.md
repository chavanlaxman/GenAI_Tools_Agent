# E-commerce Automation Framework (Python/Selenium/Pytest)

[![E-Commerce Test Automation](https://github.com/chavanlaxman/GenAI_Tools_Agent/actions/workflows/test-automation.yml/badge.svg)](https://github.com/chavanlaxman/GenAI_Tools_Agent/actions/workflows/test-automation.yml)

This framework implements automated testing for an e-commerce website using Python, Selenium WebDriver, and Pytest, following the Page Object Model (POM) pattern.

## 1. Prerequisites

- Python 3.8+
- Google Chrome browser
- Git (for version control)

## 2. Installation

```powershell
# Clone the repository
git clone https://github.com/chavanlaxman/GenAI_Tools_Agent.git
cd E-ComWebAutomation_AI

# Create and activate virtual environment (optional but recommended)
python -m venv venv
.\venv\Scripts\Activate

# Install dependencies
pip install -r requirements.txt
```

## 3. Project Structure

```
E-ComWebAutomation_AI/
├── pages/
│   ├── base_page.py           # Base page object with common utilities
│   ├── login_page/
│   │   ├── login.py           # Login page object
│   │   └── register_page.py   # Registration page object
│   ├── dashboard_page/
│   │   └── dashboard_page.py  # Dashboard/product listing page
│   └── cart_page/
│       └── cart_page.py       # Shopping cart and checkout
├── Tests/
│   ├── test_data.py          # Centralized test data
│   ├── test_login.py         # Login tests
│   ├── test_registration.py  # Registration tests
│   ├── test_dashboard.py     # Product/filter tests
│   └── test_cart.py         # Cart/checkout tests
├── conftest.py              # Pytest fixtures and configuration
├── requirements.txt         # Project dependencies
└── PROJECT_ReadMe.md       # This file
```

## 4. Key Features

1. **Page Objects**:
   - BasePage: Common utilities and element interactions
   - LoginPage: Authentication handling
   - DashboardPage: Product listing and filtering
   - CartPage: Shopping cart and checkout operations

2. **Test Organization**:
   - Modular test files by feature
   - Shared fixtures for common operations
   - Centralized test data management
   - Parameterized tests for better coverage

3. **Framework Features**:
   - Automatic webdriver management
   - HTML test reports
   - Screenshot capture on failure
   - Clean test isolation
   - Parallel test execution support

## 5. Test Execution

```powershell
# Run all tests with parallel execution (auto-detection of CPU cores)
pytest -v

# Run specific test file
pytest Tests/test_login.py -v

# Run tests with specific number of processes
pytest -v -n 4

# Run tests by marker
pytest -v -m "smoke"

# Run tests with load distribution by file
pytest -v -n auto --dist=loadfile

Note: HTML reports are generated automatically as configured in pytest.ini
```

## 6. Test Coverage

1. **User Account (UA)**:
   - Registration (new users)
   - Login/authentication
   - Profile management

2. **Product Catalog (PC)**:
   - Product search and filtering
   - Category navigation
   - Product details view

3. **Shopping Cart (SC)**:
   - Add/remove items
   - Cart management
   - Price calculations

4. **Checkout (CO)**:
   - Shipping information
   - Payment processing
   - Order confirmation

## 7. Best Practices

1. **Code Organization**:
   - One page object per page/component
   - Clean separation of concerns
   - DRY (Don't Repeat Yourself) principle

2. **Test Structure**:
   - Arrange-Act-Assert pattern
   - Clear test names and documentation
   - Independent test cases

3. **Maintenance**:
   - Centralized selectors and test data
   - Shared utilities and helpers
   - Clear error messages

## 8. Contributing

1. Create a feature branch
2. Add tests for new functionality
3. Ensure all tests pass
4. Update documentation
5. Submit pull request

## 9. CI/CD Pipeline

The project supports both GitHub Actions and Jenkins pipelines for continuous integration and delivery:

### 9.1 GitHub Actions Pipeline

1. **Automated Builds**:
   - Triggered on:
     - Push to main branch
     - Pull request to main branch
     - Daily at midnight UTC

2. **Test Execution**:
   - Runs on Windows with Chrome browser
   - Executes all test suites
   - Generates HTML test reports
   - Uploads test reports as artifacts

3. **Pipeline Features**:
   - Python environment setup
   - Chrome browser installation
   - Dependency management
   - Parallel test execution
   - Test report generation

4. **Viewing Results**:
   - Access test results in GitHub Actions
   - Download HTML reports from artifacts
   - View build status badge in README

### 9.2 Jenkins Pipeline

1. **Pipeline Structure**:
   - Located in `Jenkinsfile` at repository root
   - Shared library in `jenkins/vars/testUtils.groovy`
   - Configurable environment variables

2. **Automated Builds**:
   - Scheduled daily runs
   - Pull request triggered builds
   - Manual execution support

3. **Pipeline Stages**:
   - Environment Setup
   - Chrome Installation
   - Test Execution
   - Report Generation

4. **Features**:
   - Virtual environment management
   - Dependency installation
   - Chrome browser setup
   - HTML report generation
   - Email notifications
   - Workspace cleanup

5. **Shared Library Utilities**:
   - Python environment setup
   - Browser installation
   - Test execution
   - Report publishing
   - Email notifications
   - System requirement checks
   - Parallel test execution

6. **Viewing Results**:
   - Access Jenkins dashboard
   - View HTML test reports
   - Check email notifications
   - Download archived artifacts

## 10. Support

For issues or questions:
1. Check existing issues on GitHub
2. Create a new issue with details
3. Include test report and screenshots

## 11. Test run artifacts and logging

Each test run will create a timestamped directory under `test_logs/` with the following structure:

- test_logs/<timestamp>/
   - logs/test.log            -> Consolidated run log (INFO/DEBUG)
   - screenshots/             -> Screenshots captured on failures
   - test_results_<timestamp>.xlsx -> Excel summary of test results (name, nodeid, outcome, duration, screenshot)

How it works:
- The framework initializes a per-run folder automatically at test session start.
- A `test.log` file will capture run-level logs and errors.
- Failures will save screenshots to the `screenshots/` folder.
- After the session finishes, an Excel report is written with a row per test.

To enable and view logs locally:
```powershell
# Run tests (creates test_logs/<timestamp>/...)
pytest -q

# After run, open test_logs\<timestamp>\logs\test.log and test_results_<timestamp>.xlsx
Start-Process test_logs\<timestamp>\logs\test.log
Start-Process test_logs\<timestamp>\test_results_<timestamp>.xlsx
```