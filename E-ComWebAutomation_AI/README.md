# E-Commerce Web Automation Framework

This is an AI-powered test automation framework for E-commerce web application testing, built with Python, Pytest, and Selenium.

## Features

- Page Object Model design pattern
- Data-driven testing support
- Parallel test execution
- Comprehensive reporting
- Environment verification
- Flexible run configurations
- Cross-browser testing
- Screenshot capture on failures
- Custom test markers
- Logging system

## Prerequisites

- Python 3.8 or higher
- Chrome/Firefox browsers
- Git (for version control)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd E-ComWebAutomation_AI
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Environment Verification

Before running tests, verify your environment:

```bash
python -m utils.check_environment
```

This will check:
- Python version
- Required packages
- WebDriver availability
- Browser installations
- Directory structure

## Running Tests

Use the test runner script for different execution modes:

```bash
python run_tests.py <config-name> [additional pytest args]
```

Available configurations:
- `smoke`: Quick smoke test suite
- `regression`: Full regression suite
- `parallel`: Parallel execution mode
- `debug`: Debug mode with verbose output
- `ci`: Configuration for CI/CD pipelines

List all configurations:
```bash
python run_tests.py list
```

Examples:
```bash
# Run smoke tests
python run_tests.py smoke

# Run regression tests with extra verbosity
python run_tests.py regression -v

# Run specific test file in debug mode
python run_tests.py debug tests/test_login.py
```

## Project Structure

```
E-ComWebAutomation_AI/
│
├── conftest.py           # Pytest fixtures and configuration
├── pytest.ini           # Pytest settings and markers
├── requirements.txt     # Project dependencies
├── run_tests.py        # Test runner script
│
├── config/             # Configuration files
│   ├── browser_config.py
│   └── test_data.py
│
├── pages/              # Page Object Model classes
│   ├── __init__.py
│   ├── base_page.py
│   ├── login_page.py
│   └── ...
│
├── tests/              # Test files
│   ├── __init__.py
│   ├── test_login.py
│   └── ...
│
├── utils/              # Utility modules
│   ├── __init__.py
│   ├── check_environment.py
│   ├── run_configs.py
│   ├── test_helpers.py
│   └── ...
│
└── test_logs/         # Test execution logs and reports
```

## Custom Test Markers

Available markers:
- `@pytest.mark.smoke`: Smoke tests
- `@pytest.mark.regression`: Regression tests
- `@pytest.mark.ui`: UI tests
- `@pytest.mark.api`: API tests
- `@pytest.mark.auth`: Authentication tests

## Logging

Logs are saved in the `test_logs` directory with timestamps:
- Test execution logs
- Screenshots of failures
- HTML reports
- Environment details

## Configuration

### Browser Configuration
Configure browser settings in `config/browser_config.py`:
- Browser type
- Window size
- Timeouts
- Chrome/Firefox options

### Test Data
Manage test data in `config/test_data.py`:
- Test users
- Product data
- API endpoints
- Environment URLs

## Contributing

1. Create a feature branch
2. Write tests for new features
3. Ensure all tests pass
4. Update documentation
5. Submit pull request

## Troubleshooting

1. Environment Issues:
   - Run environment check
   - Verify Python version
   - Check package installations

2. WebDriver Issues:
   - Update browsers
   - Clear browser cache
   - Check WebDriver manager logs

3. Test Failures:
   - Check screenshots in logs
   - Review test reports
   - Verify test data
   - Check browser console logs

## Support

For support and bug reports, please create an issue in the repository.