"""Test utilities for common operations."""
import json
import os
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def take_screenshot(driver, name, screenshots_dir):
    """
    Take a screenshot and save it with timestamp.
    Args:
        driver: WebDriver instance
        name (str): Base name for the screenshot
        screenshots_dir (str): Directory to save screenshots
    Returns:
        str: Path to saved screenshot
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{name}_{timestamp}.png"
    filepath = os.path.join(screenshots_dir, filename)
    driver.save_screenshot(filepath)
    return filepath

def wait_for_toast(driver, text=None, timeout=5):
    """
    Wait for toast message and optionally verify its text.
    Args:
        driver: WebDriver instance
        text (str, optional): Expected toast message text
        timeout (int): Maximum time to wait in seconds
    Returns:
        bool: True if toast appeared with correct text (if specified)
    """
    try:
        toast = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((".toast-message", "css selector"))
        )
        if text:
            return text.lower() in toast.text.lower()
        return True
    except TimeoutException:
        return False

def save_test_artifacts(artifacts, run_dir):
    """
    Save test artifacts (data files, screenshots, etc.).
    Args:
        artifacts (dict): Dictionary of artifact name:content pairs
        run_dir (str): Directory to save artifacts
    """
    artifacts_dir = os.path.join(run_dir, 'artifacts')
    os.makedirs(artifacts_dir, exist_ok=True)
    
    for name, content in artifacts.items():
        filepath = os.path.join(artifacts_dir, name)
        if isinstance(content, (dict, list)):
            with open(filepath, 'w') as f:
                json.dump(content, f, indent=2)
        elif isinstance(content, str):
            with open(filepath, 'w') as f:
                f.write(content)
        elif isinstance(content, bytes):
            with open(filepath, 'wb') as f:
                f.write(content)

def verify_element_state(driver, locator, expected_state, timeout=10):
    """
    Verify element is in expected state (visible, enabled, selected).
    Args:
        driver: WebDriver instance
        locator (tuple): Locator tuple (By, value)
        expected_state (str): State to verify (visible/hidden/enabled/disabled/selected)
        timeout (int): Maximum time to wait
    Returns:
        bool: True if element is in expected state
    """
    wait = WebDriverWait(driver, timeout)
    try:
        if expected_state == 'visible':
            return wait.until(EC.visibility_of_element_located(locator)) is not None
        elif expected_state == 'hidden':
            return wait.until(EC.invisibility_of_element_located(locator))
        elif expected_state == 'enabled':
            element = wait.until(EC.presence_of_element_located(locator))
            return element.is_enabled()
        elif expected_state == 'disabled':
            element = wait.until(EC.presence_of_element_located(locator))
            return not element.is_enabled()
        elif expected_state == 'selected':
            element = wait.until(EC.presence_of_element_located(locator))
            return element.is_selected()
        return False
    except (TimeoutException, NoSuchElementException):
        return False

def parse_test_id(test_name):
    """
    Extract test case ID from test name/docstring.
    Args:
        test_name (str): Test name or docstring
    Returns:
        str: Test case ID or None if not found
    """
    import re
    match = re.search(r'(?:TC:|test case)\s*([A-Z]{2}_\d{2})', test_name, re.I)
    return match.group(1) if match else None