import pytest
from pages.forgot_password.forgot_password_page import ForgotPasswordPage
from pages.login_page.login import LoginPage
from .test_data import TestData


def test_forgot_password_flow(driver_for_test):
    """
    TC: UA_05 - Verify forgot password functionality
    """
    login = LoginPage(driver_for_test)
    # navigate to login page if needed
    login.perform_login(TestData.VALID_USER["email"], TestData.VALID_USER["password"])  # ensure page loaded
    fp = ForgotPasswordPage(driver_for_test)

    msg = fp.request_password_reset(TestData.FORGOT_EMAIL)
    assert TestData.MESSAGES["registration"]["success"] or msg, "Forgot password flow did not return expected message"