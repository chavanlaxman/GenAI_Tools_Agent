import pytest
from pages.product_page.product_details_page import ProductDetailsPage
from pages.dashboard_page.dashboard_page import DashboardPage
from pages.login_page.login import LoginPage
from Tests.test_data import TestData


@pytest.fixture
def setup_product_details(driver_for_test):
    """
    Fixture that provides access to a product details page.
    Returns product details page object.
    """
    # Login first
    login_page = LoginPage(driver_for_test)
    login_page.perform_login(
        TestData.VALID_USER["email"],
        TestData.VALID_USER["password"]
    )
    
    # Navigate to a product
    dashboard = DashboardPage(driver_for_test)
    product = TestData.PRODUCTS["zara_coat"]
    dashboard.view_product_details(product["title"])
    
    return ProductDetailsPage(driver_for_test)


class TestProductDetails:
    """
    Test suite for Product Details functionality.
    Covers test cases PC_05 through PC_07.
    """
    
    def test_product_details_display_pc05(self, setup_product_details):
        """
        TC: PC_05 - Verify product detail page display
        """
        product_page = setup_product_details
        expected_product = TestData.PRODUCTS["zara_coat"]
        
        # Get displayed details
        details = product_page.get_product_details()
        
        # Verify all required information is displayed
        assert details["title"] == expected_product["title"], \
            "Product title mismatch"
        assert expected_product["price"] in details["price"], \
            "Product price mismatch"
        assert expected_product["category"] in details["category"].lower(), \
            "Product category mismatch"
    
    def test_image_zoom_pc06(self, setup_product_details):
        """
        TC: PC_06 - Verify image zoom feature
        """
        product_page = setup_product_details
        
        # Trigger zoom functionality
        zoom_displayed = product_page.zoom_image()
        
        # Verify zoom view
        assert zoom_displayed, "Image zoom view not displayed"
    
    def test_review_section_pc07(self, setup_product_details):
        """
        TC: PC_07 - Verify review section functionality
        """
        product_page = setup_product_details
        
        # Get initial reviews
        initial_reviews = product_page.view_reviews()
        initial_count = len(initial_reviews)
        
        # Add a new review
        new_review = {
            "rating": 5,
            "text": "Great product, highly recommended!"
        }
        success = product_page.add_review(**new_review)
        assert success, "Failed to submit review"
        
        # Verify review was added
        updated_reviews = product_page.view_reviews()
        assert len(updated_reviews) == initial_count + 1, \
            "Review count did not increase"
        
        # Verify review details
        latest_review = updated_reviews[0]  # Assuming newest first
        assert latest_review["rating"] == new_review["rating"], \
            "Review rating mismatch"
        assert new_review["text"] in latest_review["text"], \
            "Review text mismatch"
    
    def test_thumbnail_navigation(self, setup_product_details):
        """
        Verify thumbnail image navigation
        """
        product_page = setup_product_details
        
        # Switch to second thumbnail
        success = product_page.switch_thumbnail(1)
        assert success, "Failed to switch thumbnail"
    
    def test_size_chart_pc05(self, setup_product_details):
        """
        TC: PC_05 - Verify size chart functionality
        """
        product_page = setup_product_details
        
        # Open size chart
        size_chart_displayed = product_page.open_size_chart()
        assert size_chart_displayed, "Size chart not displayed"
    
    def test_size_selection(self, setup_product_details):
        """
        Verify size selection functionality
        """
        product_page = setup_product_details
        
        # Select a size
        success = product_page.select_size("M")
        assert success, "Failed to select size"
    
    @pytest.mark.parametrize("rating", [1, 3, 5])
    def test_different_ratings_pc07(self, setup_product_details, rating):
        """
        TC: PC_07 - Verify different rating submissions
        """
        product_page = setup_product_details
        
        # Submit review with different ratings
        success = product_page.add_review(
            rating=rating,
            text=f"Test review with {rating} star rating"
        )
        assert success, f"Failed to submit {rating}-star review"
