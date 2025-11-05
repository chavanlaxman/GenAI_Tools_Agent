from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class BasePage:
    """
    Base page object that all page objects should inherit from.
    Contains common utilities and helper methods.
    """
    # Common toast message locator
    TOAST_MESSAGE = (By.CSS_SELECTOR, ".toast-message")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def wait_and_find_element(self, locator):
        """Wait for and return an element."""
        return self.wait.until(EC.presence_of_element_located(locator))

    def wait_and_click(self, locator):
        """Wait for and click an element."""
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def fill_input(self, locator, text):
        """Wait for, find, and fill an input field."""
        element = self.wait_and_find_element(locator)
        element.clear()  # Clear existing text
        element.send_keys(text)

    def get_toast_message(self):
        """Get text from toast message notification."""
        return self.wait.until(EC.presence_of_element_located(self.TOAST_MESSAGE)).text

    def is_toast_message_present(self, timeout=5):
        """Check if toast message is present."""
        try:
            self.wait = WebDriverWait(self.driver, timeout)
            self.wait.until(EC.presence_of_element_located(self.TOAST_MESSAGE))
            return True
        except:
            return False
        finally:
            self.wait = WebDriverWait(self.driver, 10)  # Reset to default timeout