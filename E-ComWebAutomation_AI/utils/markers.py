# pytest markers for the test framework
import pytest

# Test Categories
smoke = pytest.mark.smoke
regression = pytest.mark.regression
ui = pytest.mark.ui
api = pytest.mark.api

# Test Priority and Status
critical = pytest.mark.critical
flaky = pytest.mark.flaky
slow = pytest.mark.slow

# Feature Areas
login = pytest.mark.login
cart = pytest.mark.cart
payment = pytest.mark.payment
social = pytest.mark.social

# Test Requirements
requires_auth = pytest.mark.requires_auth
requires_data = pytest.mark.requires_data

# Test Environment
production = pytest.mark.production
staging = pytest.mark.staging
qa = pytest.mark.qa

# Browser Specific
chrome_only = pytest.mark.chrome_only
firefox_only = pytest.mark.firefox_only

# Custom Markers
parallel_safe = pytest.mark.parallel_safe
skip_in_ci = pytest.mark.skip_in_ci

# Example usage in test files:
"""
from markers import smoke, critical, login

@smoke
@critical
@login
def test_user_login():
    pass
"""