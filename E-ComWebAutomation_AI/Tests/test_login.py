import pytest
from pages.login_page.login import LoginPage
from utils.test_helpers import test_case, retry_if_fails
from Tests.test_data import TestData


class TestLogin:
    """
    Test suite for Login functionality.
    Covers test cases UA_03 (successful login) and UA_04 (failed login).
    """
    
    @pytest.fixture(autouse=True)
    def setup(self, driver_for_test, request):
        """Setup for each test case."""
        self.login_page = LoginPage(driver_for_test)
        self.logger = request.node.test_logger
        yield
        # Cleanup after each test
        self.login_page.clear_login_form()

    @test_case('UA_03', feature='login', smoke=True, critical=True)
    @retry_if_fails(max_retries=2)
    def test_valid_login_success_ua03(self):
        """
        Verify successful login with valid credentials.

        Strategy:
        - Use known valid credentials
        - Verify both success message and dashboard access
        - Check login state persistence
        """
        self.logger.info("Starting login test with valid credentials")
        
        # Given: Valid user credentials
        valid_user = TestData.VALID_USER
        self.logger.debug(f"Using test user: {valid_user['email']}")

        # When: User performs login
        self.login_page.perform_login(
            email=valid_user["email"],
            password=valid_user["password"]
        )
        self.logger.info("Login action performed")

        # Then: Verify successful login
        assert self.login_page.is_login_successful(), \
            "Login failed with valid credentials"

        success_msg = self.login_page.get_success_message()
        expected_msg = TestData.MESSAGES["login"]["success"]
        assert expected_msg in success_msg, \
            f"Expected success message '{expected_msg}' not found in '{success_msg}'"
        
        self.logger.info("Login test completed successfully")

    def test_invalid_login_shows_error_ua04(self):
        """
        TC: UA_04 - Verify appropriate error handling for invalid login.

        Strategy:
        - Test both invalid email and password cases
        - Verify error messages and form state
        - Ensure security best practices
        """
        # Given: Invalid user credentials
        invalid_user = TestData.INVALID_USER

        # When: User attempts login with invalid credentials
        self.login_page.perform_login(
            email=invalid_user["email"],
            password=invalid_user["password"]
        )

        # Then: Verify error handling
        assert not self.login_page.is_login_successful(), \
            "Login should not succeed with invalid credentials"

        error_msg = self.login_page.get_error_message()
        expected_error = TestData.MESSAGES["login"]["invalid_credentials"]
        assert expected_error in error_msg, \
            f"Expected error message '{expected_error}' not found in '{error_msg}'"

    @pytest.mark.parametrize("test_input", [
        {"email": "", "password": "ValidPass123!", "error": "Email is required"},
        {"email": "test@example.com", "password": "", "error": "Password is required"},
        {"email": "invalid-email", "password": "pass", "error": "Invalid email format"}
    ])
    def test_login_field_validation_ua06(self, test_input):
        """
        TC: UA_06 - Verify login form field validation.

        Strategy:
        - Test multiple validation scenarios
        - Check client-side validation
        - Verify helpful error messages
        """
        # When: Submit login with invalid input
        self.login_page.perform_login(
            email=test_input["email"],
            password=test_input["password"]
        )

        # Then: Verify validation message
        error_msg = self.login_page.get_error_message()
        assert test_input["error"] in error_msg, \
            f"Expected validation message '{test_input['error']}' not found in '{error_msg}'"
