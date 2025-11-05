from pages.login_page.login import LoginPage
from pages.dashboard_page.dashboard_page import DashboardPage
from .test_data import TestData


def test_logout_functionality(driver_for_test):
    """
    TC: UA_09 - Verify logout functionality
    """
    login = LoginPage(driver_for_test)
    login.perform_login(TestData.VALID_USER["email"], TestData.VALID_USER["password"])

    dashboard = DashboardPage(driver_for_test)
    dashboard.sign_out()

    # After logout should redirect to login page or not show dashboard header
    assert "auth/login" in driver_for_test.current_url or not dashboard.is_toast_message_present(), "Logout may not have worked"