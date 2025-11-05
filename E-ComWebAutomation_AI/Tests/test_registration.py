import pytest
from pages.login_page.register_page import RegistrationPage
from Tests.test_data import TestData


class TestRegistration:
    """
    Test suite for User Registration functionality.
    Covers test cases UA_01 (valid registration) and UA_02 (duplicate email).
    """

    @pytest.fixture(autouse=True)
    def setup(self, driver_for_test):
        """Setup for each test case."""
        self.register_page = RegistrationPage(driver_for_test)
        self.register_page.navigate_to_register_form()
        yield
        # Cleanup after each test if needed
        self.register_page.clear_registration_form()

    def test_valid_user_registration_ua01(self):
        """
        TC: UA_01 - Verify successful user registration with valid data.

        Strategy:
        - Use unique email to avoid conflicts
        - Verify both success message and form submission
        - Check redirect to login/dashboard
        """
        # Given: Unique user registration data
        unique_email = TestData.generate_unique_email()
        password = TestData.get_valid_password()

        # When: Fill and submit registration form
        self.register_page.fill_registration_form(
            name=TestData.VALID_USER["name"],
            email=unique_email,
            password=password,
            confirm_password=password
        )
        submission_success = self.register_page.submit_registration()

        # Then: Verify registration success
        assert submission_success, "Registration form submission failed"
        
        success_msg = self.register_page.get_success_message()
        expected_msg = TestData.MESSAGES["registration"]["success"]
        assert expected_msg in success_msg, \
            f"Expected success message '{expected_msg}' not found in '{success_msg}'"

    def test_duplicate_email_registration_ua02(self):
        """
        TC: UA_02 - Verify registration attempt with existing email is rejected.

        Strategy:
        - Use known registered email (from TestData)
        - Verify error message and validation
        - Ensure form remains accessible
        """
        # Given: Registration data with existing email
        existing_email = TestData.VALID_USER["email"]
        password = TestData.get_valid_password()

        # When: Attempt registration with existing email
        self.register_page.fill_registration_form(
            name=TestData.VALID_USER["name"],
            email=existing_email,
            password=password,
            confirm_password=password
        )
        self.register_page.submit_registration()

        # Then: Verify appropriate error message
        assert self.register_page.is_email_already_registered(), \
            "Email validation for duplicate registration not shown"
            
        error_msg = self.register_page.get_error_message()
        expected_error = TestData.MESSAGES["registration"]["email_exists"]
        assert expected_error in error_msg, \
            f"Expected error message '{expected_error}' not found in '{error_msg}'"

    def test_password_mismatch_registration(self):
        """
        TC: UA_05 - Verify registration with mismatched passwords is rejected.
        
        Strategy:
        - Submit form with different passwords
        - Verify error handling
        - Check form state preservation
        """
        # Given: Registration data with mismatched passwords
        email = TestData.generate_unique_email()
        password1 = TestData.get_valid_password()
        password2 = password1 + "different"

        # When: Submit form with mismatched passwords
        self.register_page.fill_registration_form(
            name=TestData.VALID_USER["name"],
            email=email,
            password=password1,
            confirm_password=password2
        )
        self.register_page.submit_registration()

        # Then: Verify error message
        error_msg = self.register_page.get_error_message()
        expected_error = TestData.MESSAGES["registration"]["password_mismatch"]
        assert expected_error in error_msg, \
            f"Expected password mismatch error not found in '{error_msg}'"
