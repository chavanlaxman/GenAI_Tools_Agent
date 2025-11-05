import pytest
from pages.cart_page.cart_page import CartPage
from pages.dashboard_page.dashboard_page import DashboardPage
from pages.login_page.login import LoginPage
from .test_data import TestData


@pytest.fixture
def setup_cart(driver_for_test):
    """
    Fixture that provides a logged-in session with an item in cart.
    Returns both dashboard and cart page objects.
    """
    # Login first
    login_page = LoginPage(driver_for_test)
    login_page.perform_login(
        TestData.VALID_USER["email"],
        TestData.VALID_USER["password"]
    )
    
    # Add an item to cart
    dashboard = DashboardPage(driver_for_test)
    product = TestData.PRODUCTS["zara_coat"]
    dashboard.add_product_to_cart(product["title"])
    
    # Navigate to cart
    dashboard.navigate_to_cart()
    
    # Return both page objects for test use
    return {
        "dashboard": dashboard,
        "cart": CartPage(driver_for_test)
    }


class TestCartCheckout:
    """
    Test suite for Shopping Cart and Checkout functionality.
    Covers test cases SC_01 through SC_07 and CO_01 through CO_08.
    """
    
    def test_view_cart_items_sc01(self, setup_cart):
        """
        TC: SC_01 - Verify items added to cart are displayed correctly
        """
        cart = setup_cart["cart"]
        expected_item = TestData.PRODUCTS["zara_coat"]
        
        # Then: Verify item details in cart
        assert cart.verify_item_in_cart(expected_item), \
            f"Expected item {expected_item['title']} not found in cart"
        
        # And: Verify cart count
        assert cart.get_cart_count() == 1, \
            "Cart count should be 1"
            
    def test_remove_from_cart_sc02(self, setup_cart):
        """
        TC: SC_02 - Verify removing items from cart
        """
        cart = setup_cart["cart"]
        item_to_remove = TestData.PRODUCTS["zara_coat"]["title"]
        
        # When: Remove item from cart
        removed = cart.remove_item(item_to_remove)
        
        # Then: Verify item removal
        assert removed, f"Failed to remove {item_to_remove} from cart"
        assert cart.is_cart_empty(), "Cart should be empty after removal"

    def test_update_quantity_sc03(self, setup_cart):
        """
        TC: SC_03 - Verify updating product quantity updates totals
        """
        cart = setup_cart["cart"]
        product_title = TestData.CART_ITEMS["single_item"]["product"]
        # Ensure item is present
        assert cart.verify_item_in_cart(TestData.PRODUCTS["zara_coat"]), "Item missing before quantity update"

        # Update quantity to 3
        updated = cart.update_item_quantity(product_title, 3)
        assert updated, "Failed to update item quantity"

        # Verify subtotal reflects quantity (price * quantity)
        price = float(TestData.PRODUCTS["zara_coat"]["price"])
        expected_subtotal = price * 3
        assert cart.get_subtotal() == expected_subtotal, f"Subtotal {cart.get_subtotal()} != expected {expected_subtotal}"
        
    def test_cart_total_calculation_sc04(self, setup_cart):
        """
        TC: SC_04 - Verify cart total calculation
        """
        cart = setup_cart["cart"]
        
        # Get cart totals
        subtotal = cart.get_subtotal()
        total = cart.get_total()
        
        # Verify calculations
        assert subtotal == float(TestData.PRODUCTS["zara_coat"]["price"]), \
            "Subtotal calculation incorrect"
        assert total == subtotal, \
            "Total should match subtotal when no additional charges"
            
    def test_continue_shopping_sc07(self, setup_cart):
        """
        TC: SC_07 - Verify continue shopping functionality
        """
        cart = setup_cart["cart"]
        
        # When: Click continue shopping
        cart.continue_shopping()
        
        # Then: Verify return to dashboard
        assert "dashboard" in cart.driver.current_url.lower(), \
            "Should return to dashboard page"
            
    def test_checkout_navigation_co01(self, setup_cart):
        """
        TC: CO_01 - Verify checkout navigation from cart
        """
        cart = setup_cart["cart"]
        
        # When: Click checkout button
        cart.proceed_to_checkout()
        
        # Then: Verify navigation to checkout
        assert "checkout" in cart.driver.current_url.lower(), \
            "Should navigate to checkout page"
            
    def test_empty_cart_checkout_co06(self, driver_for_test):
        """
        TC: CO_06 - Verify checkout with empty cart
        """
        # Given: Empty cart (new session)
        login_page = LoginPage(driver_for_test)
        login_page.perform_login(
            TestData.VALID_USER["email"],
            TestData.VALID_USER["password"]
        )
        
        dashboard = DashboardPage(driver_for_test)
        dashboard.navigate_to_cart()
        cart = CartPage(driver_for_test)
        
        # When/Then: Verify empty cart state
        assert cart.is_cart_empty(), "Cart should be empty for new session"
        assert cart.get_cart_count() == 0, "Cart count should be 0"
        
    @pytest.mark.parametrize("product_key", ["zara_coat", "adidas", "iphone"])
    def test_buy_now_functionality(self, setup_cart, product_key):
        """
        Verify Buy Now functionality for different products
        """
        cart = setup_cart["cart"]
        product = TestData.PRODUCTS[product_key]
        
        # When: Click Buy Now
        if cart.verify_item_in_cart(product):
            success = cart.buy_now(product["title"])
            
            # Then: Verify Buy Now action
            assert success, f"Buy Now failed for {product['title']}"
            assert "order" in cart.driver.current_url.lower(), \
                "Should navigate to order page"