import os
import time
import pytest
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from openpyxl import Workbook
from utils.logger import init_logger

from utils.config import TestConfig
from utils.test_utils import take_screenshot, save_test_artifacts
from utils.report_helper import create_excel_report, cleanup_old_reports, consolidate_run_logs

# Global variables
logger = None
test_config = None


def pytest_configure(config):
    """
    Custom pytest configuration for test execution.
    Sets up logging, directories, and configuration.
    """
    # Initialize test configuration
    global test_config
    test_config = TestConfig()
    
    # Create timestamp for this run
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Create run directory structure
    logs_root = os.path.abspath('test_logs')
    os.makedirs(logs_root, exist_ok=True)
    run_dir = os.path.join(logs_root, timestamp)
    os.makedirs(run_dir, exist_ok=True)
    os.makedirs(os.path.join(run_dir, 'screenshots'), exist_ok=True)
    os.makedirs(os.path.join(run_dir, 'logs'), exist_ok=True)
    os.makedirs(os.path.join(run_dir, 'artifacts'), exist_ok=True)

    # Attach run info to config
    config._run_dir = run_dir
    config._run_timestamp = timestamp
    config._test_config = test_config

    # Initialize logger
    global logger
    logger = init_logger(run_dir)
    logger.info(f"Test run directory created: {run_dir}")

    # Configure test session metadata
    metadata = {
        'Timestamp': timestamp,
        'Environment': os.getenv('TEST_ENV', 'qa'),
        'Browser': 'Chrome',
        'Parallel': str(test_config.get('test', 'parallel')),
        'Headless': str(test_config.get('browser', 'headless'))
    }
    
    # Add metadata entries as individual items
    for key, value in metadata.items():
        config.stash[f'metadata/{key}'] = value

    # Set parallel workers if enabled
    if test_config.get('test', 'parallel'):
        workers = test_config.get('test', 'max_workers')
        if workers != 'auto':
            config.option.numprocesses = int(workers)

    # Clean up old reports
    cleanup_old_reports(logs_root)

    # create container for test results that will be written to Excel
    config._test_results = []

@pytest.fixture(scope="function")
def setup_driver(request, browser_config):
    """
    Sets up the Chrome WebDriver instance using webdriver_manager.
    This fixture is function-scoped for parallel execution support.
    Uses browser_config fixture for configuration.
    """
    # Configure Chrome options
    chrome_options = Options()
    chrome_options.page_load_strategy = 'none'  # Don't wait for full page load
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-software-rasterizer')
    chrome_options.add_argument('--disk-cache-size=0')  # Disable disk cache
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])  # Reduce logging
    
    # Apply browser config
    if browser_config['headless']:
        chrome_options.add_argument('--headless=new')  # new headless mode
    
    # Set viewport size
    chrome_options.add_argument(f"--window-size={browser_config['viewport_width']},{browser_config['viewport_height']}")
    
    # Try to use an existing ChromeDriver if available
    driver_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chromedriver.exe")
    
    if not os.path.exists(driver_path):
        try:
            driver_path = ChromeDriverManager().install()
        except Exception as e:
            logger.error(f"Failed to install ChromeDriver: {str(e)}")
            pytest.skip("ChromeDriver installation failed")
    
    # Create ChromeService with the driver path
    service = ChromeService(driver_path)
    
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(browser_config['timeout'])
    
    if not browser_config['headless']:
        driver.maximize_window()
    
    # Store the driver in the request context for screenshots
    request.instance.driver = driver
    
    yield driver
    
    # Capture screenshot on test failure (best-effort — main capture happens in makereport)
    try:
        if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            run_dir = getattr(request.config, '_run_dir', os.path.abspath('test_logs'))
            screenshots_dir = os.path.join(run_dir, 'screenshots')
            screenshot_name = os.path.join(screenshots_dir, f"failed_{request.node.name}_{timestamp}.png")
            driver.save_screenshot(screenshot_name)
            if logger:
                logger.error(f"Saved failure screenshot (teardown): {screenshot_name}")
    except Exception:
        pass
    
    # Teardown: close the browser after each test
    driver.quit()

@pytest.fixture(scope="session")
def base_url():
    """
    Defines the base URL for the application.
    Can be overridden by environment variables.
    Session scope - created once for all tests.
    """
    return os.getenv('TEST_BASE_URL', 
                     "https://rahulshettyacademy.com/client/#/auth/login")

@pytest.fixture(scope="module")
def browser_config():
    """
    Module-scoped fixture for browser configuration.
    Same browser config will be used for all tests in a module.
    """
    config = {
        'headless': os.getenv('TEST_HEADLESS', 'true').lower() == 'true',
        'viewport_width': int(os.getenv('TEST_VIEWPORT_WIDTH', 1920)),
        'viewport_height': int(os.getenv('TEST_VIEWPORT_HEIGHT', 1080)),
        'timeout': int(os.getenv('TEST_TIMEOUT', 10))
    }
    return config

@pytest.fixture(scope="class")
def user_credentials():
    """
    Class-scoped fixture for test user credentials.
    Same user will be used for all tests in a class.
    """
    return {
        'email': os.getenv('TEST_USER_EMAIL', 'test.qa@shop.com'),
        'password': os.getenv('TEST_USER_PASSWORD', 'ValidPassword123!')
    }

@pytest.fixture(scope="session")
def test_data_dir(request):
    """
    Session-scoped fixture for test data directory.
    Creates and provides path to test data directory.
    """
    data_dir = os.path.join(request.config._run_dir, 'test_data')
    os.makedirs(data_dir, exist_ok=True)
    return data_dir

@pytest.fixture(scope="function")
def driver_for_test(setup_driver, base_url, user_credentials):
    """
    A function-scoped fixture that navigates to the base URL before each test.
    The credentials from the user_credentials fixture are attached to
    the driver instance for easy access in tests.
    """
    driver = setup_driver
    driver.user_credentials = user_credentials  # Attach credentials to driver
    driver.get(base_url)
    return driver

def pytest_runtest_setup(item):
    # record start time for the test
    item._start_time = time.time()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Extends the PyTest Plugin to track test status and save screenshots on failure.
    Collects test results into config._test_results for Excel export at session finish.
    """
    outcome = yield
    rep = outcome.get_result()

    # attach report to item for other fixtures
    setattr(item, "rep_" + rep.when, rep)

    # Only collect the call phase (the test function execution)
    if rep.when == 'call':
        start = getattr(item, '_start_time', None)
        end = time.time()
        duration = None
        if start:
            duration = round(end - start, 3)

        # default screenshot path
        screenshot_path = ''
        try:
            driver = item.funcargs.get('driver_for_test') or getattr(item.instance, 'driver', None)
            if rep.failed and driver:
                ts = datetime.now().strftime('%Y%m%d_%H%M%S')
                run_dir = getattr(item.config, '_run_dir', os.path.abspath('test_logs'))
                screenshots_dir = os.path.join(run_dir, 'screenshots')
                screenshot_path = os.path.join(screenshots_dir, f"failed_{item.name}_{ts}.png")
                try:
                    driver.save_screenshot(screenshot_path)
                    if logger:
                        logger.error(f"Saved failure screenshot: {screenshot_path}")
                except Exception:
                    screenshot_path = ''
        except Exception:
            screenshot_path = ''

        # collect result
        result = {
            'nodeid': item.nodeid,
            'name': item.name,
            'outcome': rep.outcome,
            'duration': duration,
            'screenshot': screenshot_path,
        }
        try:
            item.config._test_results.append(result)
        except Exception:
            pass


def pytest_sessionfinish(session, exitstatus):
    """Write collected test results to an Excel file in the run directory."""
    try:
        run_dir = getattr(session.config, '_run_dir', None)
        if not run_dir:
            return
        results = getattr(session.config, '_test_results', [])
        if not results:
            # nothing to write
            return

        wb = Workbook()
        ws = wb.active
        ws.title = 'Test Results'
        headers = ['name', 'nodeid', 'outcome', 'duration', 'screenshot']
        ws.append(headers)
        for r in results:
            ws.append([r.get(h, '') for h in headers])

        excel_path = os.path.join(run_dir, f"test_results_{session.config._run_timestamp}.xlsx")
        wb.save(excel_path)
        if logger:
            logger.info(f"Saved Excel test results: {excel_path}")
    except Exception as e:
        if logger:
            logger.exception('Failed to write Excel test results')