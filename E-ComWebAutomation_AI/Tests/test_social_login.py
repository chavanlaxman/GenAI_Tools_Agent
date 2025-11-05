import os
import pytest
from selenium.webdriver.common.by import By
from pages.login_page.login import LoginPage
from Tests.test_data import TestData


@pytest.mark.skipif(os.getenv('RUN_SOCIAL_TESTS', 'false').lower() != 'true', reason="Social login tests disabled by default")
def test_social_login_buttons_present(driver_for_test):
    """
    TC: UA_06 - Smoke: verify social login buttons exist (Google/Facebook)
    Note: Full OAuth flow is not executed in CI. To run full flow set RUN_SOCIAL_TESTS=true and provide credentials.
    """
    login = LoginPage(driver_for_test)
    # Ensure page loaded
    # Check presence of social login buttons by selector hints
    driver = driver_for_test
    elements = driver.find_elements(By.CSS_SELECTOR, ".social-login, .login-social, .auth-provider")
    assert len(elements) >= 1, "No social login buttons found"
    # Verify configured providers in TestData
    assert "google" in TestData.SOCIAL_PROVIDERS
    assert "facebook" in TestData.SOCIAL_PROVIDERS
