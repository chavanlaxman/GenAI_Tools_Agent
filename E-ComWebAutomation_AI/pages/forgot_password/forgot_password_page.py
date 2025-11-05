from selenium.webdriver.common.by import By
from ..base_page import BasePage

class ForgotPasswordPage(BasePage):
    """
    Page object for Forgot Password functionality (UA_05).
    """
    FORGOT_LINK = (By.LINK_TEXT, "Forgot Password")
    EMAIL_INPUT = (By.CSS_SELECTOR, "input[type='email'], input[name='email']")
    SUBMIT_BTN = (By.CSS_SELECTOR, "button[type='submit'], .btn-submit")
    SUCCESS_TOAST = (By.CSS_SELECTOR, ".toast-message")

    def navigate_to_forgot(self):
        try:
            self.wait_and_click(self.FORGOT_LINK)
            return True
        except:
            return False

    def submit_email(self, email):
        self.fill_input(self.EMAIL_INPUT, email)
        self.wait_and_click(self.SUBMIT_BTN)

    def get_success_message(self):
        if self.is_toast_message_present():
            return self.get_toast_message()
        return ""

    def request_password_reset(self, email):
        """Full flow: navigate, submit and return success message."""
        if not self.navigate_to_forgot():
            # If forgot page is directly reachable via route
            try:
                self.driver.get(self.driver.current_url + "#/auth/forgotpassword")
            except:
                pass
        self.submit_email(email)
        return self.get_success_message()
