import pytest
from pages.dashboard_page.dashboard_page import DashboardPage
from pages.login_page.login import LoginPage
from Tests.test_data import TestData


@pytest.fixture
def dashboard_page(driver_for_test):
    """
    Fixture that provides a logged-in dashboard page.
    Handles login and returns the dashboard page object.
    """
    # First login
    login_page = LoginPage(driver_for_test)
    login_page.perform_login(
        TestData.VALID_USER["email"],
        TestData.VALID_USER["password"]
    )
    
    # Return dashboard page object
    return DashboardPage(driver_for_test)


class TestDashboard:
    """
    Test suite for Dashboard functionality.
    Covers filtering, product viewing, and cart operations.
    """
    
    def test_product_search_pc01(self, dashboard_page):
        """
        TC: PC_01 - Verify product search functionality
        """
        # When: Search for a specific product
        dashboard_page.search_products("ZARA")
        
        # Then: Verify search results
        products = dashboard_page.get_product_details()
        assert any("ZARA" in product["title"].upper() for product in products), \
            "Search results should contain ZARA products"
            
    def test_price_filter_pc04(self, dashboard_page):
        """
        TC: PC_04 - Verify price range filter
        """
        # When: Set price range
        dashboard_page.set_price_range("10000", "20000")
        
        # Then: Verify filtered products are within range
        products = dashboard_page.get_product_details()
        for product in products:
            price = float(product["price"])
            assert 10000 <= price <= 20000, \
                f"Product price {price} is outside the filtered range"
                
    def test_category_filter_pc01(self, dashboard_page):
        """
        TC: PC_01 - Verify category filtering
        """
        # When: Select electronics category
        dashboard_page.select_category("electronics")
        
        # Then: Verify products are from electronics category
        products = dashboard_page.get_product_details()
        assert len(products) > 0, "Should show electronics products"
        
    @pytest.mark.parametrize("subcategory", ["mobiles", "laptops"])
    def test_subcategory_filter(self, dashboard_page, subcategory):
        """
        TC: PC_01 - Verify subcategory filtering
        """
        # When: Select a subcategory
        dashboard_page.select_subcategory(subcategory)
        
        # Then: Verify products match subcategory
        products = dashboard_page.get_product_details()
        assert len(products) > 0, f"Should show {subcategory} products"
        
    def test_add_to_cart_sc01(self, dashboard_page):
        """
        TC: SC_01 - Verify adding product to cart
        """
        # Given: A specific product title
        product_title = "ZARA COAT 3"
        
        # When: Add product to cart
        added = dashboard_page.add_product_to_cart(product_title)
        
        # Then: Verify product was added
        assert added, f"Failed to add {product_title} to cart"
        assert dashboard_page.is_toast_message_present(), \
            "Should show confirmation message"
            
    def test_view_product_details_pc05(self, dashboard_page):
        """
        TC: PC_05 - Verify product detail view
        """
        # Given: A specific product
        product_title = "iphone 13 pro"
        
        # When: View product details
        viewed = dashboard_page.view_product_details(product_title)
        
        # Then: Verify product details are shown
        assert viewed, f"Failed to view details for {product_title}"
        
    def test_results_count_display(self, dashboard_page):
        """
        Verify results count matches displayed products
        """
        # When: Get results count and actual product count
        count_text = dashboard_page.get_results_count_text()
        actual_count = dashboard_page.get_product_count()
        
        # Then: Verify counts match
        expected_count = int(count_text.split()[1])  # "Showing X results"
        assert expected_count == actual_count, \
            f"Results count {expected_count} doesn't match actual products {actual_count}"
            
    def test_navigation_buttons(self, dashboard_page):
        """
        Verify navigation button functionality
        """
        # Test Orders navigation
        dashboard_page.navigate_to_orders()
        assert "orders" in dashboard_page.driver.current_url.lower()
        
        # Test Cart navigation
        dashboard_page.navigate_to_cart()
        assert "cart" in dashboard_page.driver.current_url.lower()
        
    @pytest.mark.parametrize("test_data", [
        {"min": "1000", "max": "5000"},
        {"min": "5000", "max": "20000"},
        {"min": "20000", "max": "100000"}
    ])
    def test_price_range_combinations(self, dashboard_page, test_data):
        """
        Test different price range combinations
        """
        # When: Set price range
        dashboard_page.set_price_range(test_data["min"], test_data["max"])
        
        # Then: Verify products are filtered
        products = dashboard_page.get_product_details()
        if products:  # If any products found
            min_price = float(test_data["min"])
            max_price = float(test_data["max"])
            for product in products:
                price = float(product["price"])
                assert min_price <= price <= max_price, \
                    f"Product price {price} outside range {min_price}-{max_price}"
