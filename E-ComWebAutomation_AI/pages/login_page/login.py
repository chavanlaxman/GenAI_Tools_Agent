from selenium.webdriver.common.by import By
from ..base_page import BasePage


class LoginPage(BasePage):
    """
    Page Object Model for the E-commerce Login Page.
    Handles authentication logic for test cases UA_03 and UA_04.
    """
    # --- Locators ---
    EMAIL_FIELD = (By.ID, "userEmail")
    PASSWORD_FIELD = (By.ID, "userPassword")
    LOGIN_BUTTON = (By.ID, "login")
    DASHBOARD_HEADER = (By.CSS_SELECTOR, ".dashboard-header")  # Add a more reliable success indicator

    def perform_login(self, email, password):
        """
        Performs the login action with given credentials.
        Args:
            email (str): User's email address
            password (str): User's password
        """
        self.fill_input(self.EMAIL_FIELD, email)
        self.fill_input(self.PASSWORD_FIELD, password)
        self.wait_and_click(self.LOGIN_BUTTON)

    def get_error_message(self):
        """
        Retrieves the login error message when credentials are invalid.
        Returns:
            str: The error message text
        """
        return self.get_toast_message()

    def is_login_successful(self):
        """
        Checks if login was successful by looking for dashboard elements.
        Returns:
            bool: True if login succeeded, False otherwise
        """
        try:
            # First check for success toast
            if not self.is_toast_message_present():
                return False
            
            # Then verify we're on the dashboard
            self.wait.until(EC.presence_of_element_located(self.DASHBOARD_HEADER))
            return True
        except:
            return False

    def clear_login_form(self):
        """Clears the login form fields."""
        self.wait_and_find_element(self.EMAIL_FIELD).clear()
        self.wait_and_find_element(self.PASSWORD_FIELD).clear()