import pytest
from pages.dashboard_page.dashboard_page import DashboardPage
from pages.login_page.login import LoginPage
from Tests.test_data import TestData


@pytest.fixture
def setup_recommendations(driver_for_test):
    login = LoginPage(driver_for_test)
    login.perform_login(TestData.VALID_USER["email"], TestData.VALID_USER["password"])
    return DashboardPage(driver_for_test)


def test_recommendations_update_after_browsing_pc08(setup_recommendations):
    """
    TC: PC_08 - Verify personalized recommendations update after browsing
    """
    dashboard = setup_recommendations
    # Browse a fashion product to influence recommendations
    dashboard.browse_product_for_recommendation("ZARA COAT 3")

    recs = dashboard.get_recommendations()
    # At least one recommended item from fashion should exist
    titles = [r["title"] for r in recs]
    assert any(expected in titles for expected in TestData.RECOMMENDATIONS.get("fashion", [])), \
        "Recommendations did not update for category 'fashion'"
