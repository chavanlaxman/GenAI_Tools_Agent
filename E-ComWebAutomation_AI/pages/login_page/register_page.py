from selenium.webdriver.common.by import By
from ..base_page import BasePage


class RegistrationPage(BasePage):
    """
    Page Object Model for the User Registration Page.
    Handles test cases UA_01 (successful registration) and UA_02 (duplicate email).
    """
    # --- Locators ---
    REGISTER_LINK = (By.LINK_TEXT, "Register")
    FULL_NAME_FIELD = (By.ID, "userName")
    EMAIL_FIELD = (By.ID, "userEmail")
    PASSWORD_FIELD = (By.ID, "userPassword")
    CONFIRM_PASSWORD_FIELD = (By.ID, "confirmPassword")
    REGISTER_BUTTON = (By.ID, "login")
    
    # Field validation messages
    PASSWORD_VALIDATION = (By.CSS_SELECTOR, ".password-validation")
    EMAIL_VALIDATION = (By.CSS_SELECTOR, ".email-validation")

    def navigate_to_register_form(self):
        """
        Navigates from the login screen to the registration form.
        """
        self.wait_and_click(self.REGISTER_LINK)

    def fill_registration_form(self, name, email, password, confirm_password):
        """
        Fills out the registration form fields.
        Args:
            name (str): User's full name
            email (str): User's email address
            password (str): Chosen password
            confirm_password (str): Password confirmation
        """
        self.fill_input(self.FULL_NAME_FIELD, name)
        self.fill_input(self.EMAIL_FIELD, email)
        self.fill_input(self.PASSWORD_FIELD, password)
        self.fill_input(self.CONFIRM_PASSWORD_FIELD, confirm_password)

    def submit_registration(self):
        """
        Submits the registration form.
        Returns:
            bool: True if submission was successful
        """
        self.wait_and_click(self.REGISTER_BUTTON)
        return self.is_toast_message_present()

    def get_success_message(self):
        """
        Retrieves the registration success message.
        Returns:
            str: Success message text
        """
        return self.get_toast_message()

    def get_error_message(self):
        """
        Retrieves the registration error message.
        Returns:
            str: Error message text
        """
        return self.get_toast_message()

    def is_email_already_registered(self):
        """
        Checks if the email validation shows 'already registered' message.
        Returns:
            bool: True if email is already registered
        """
        try:
            validation = self.wait_and_find_element(self.EMAIL_VALIDATION)
            return "already registered" in validation.text.lower()
        except:
            return False

    def clear_registration_form(self):
        """Clears all registration form fields."""
        for field in [self.FULL_NAME_FIELD, self.EMAIL_FIELD, 
                     self.PASSWORD_FIELD, self.CONFIRM_PASSWORD_FIELD]:
            self.wait_and_find_element(field).clear()