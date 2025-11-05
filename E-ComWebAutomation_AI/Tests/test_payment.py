import pytest
from pages.payment_page.payment_page import PaymentPage
from pages.cart_page.cart_page import CartPage
from pages.login_page.login import LoginPage
from .test_data import TestData


@pytest.fixture
def setup_payment(driver_for_test):
    """
    Fixture that provides a logged-in session with items in cart ready for payment.
    Returns payment page object.
    """
    # Login first
    login_page = LoginPage(driver_for_test)
    login_page.perform_login(
        TestData.VALID_USER["email"],
        TestData.VALID_USER["password"]
    )
    
    # Navigate to cart and proceed to payment
    cart = CartPage(driver_for_test)
    cart.navigate_to_cart()
    cart.proceed_to_checkout()
    
    return PaymentPage(driver_for_test)


class TestPaymentAndOrder:
    """
    Test suite for Payment and Order Placement functionality.
    Covers test cases PY_01 through PY_10.
    """
    
    def test_verify_product_details_py01(self, setup_payment):
        """
        TC: PY_01 - Verify product details on payment page
        """
        payment_page = setup_payment
        expected_product = {
            "title": "ZARA COAT 3",
            "price": "11500",
            "quantity": "1"
        }
        
        # Verify product details
        assert payment_page.verify_product_details(expected_product), \
            "Product details do not match on payment page"
            
    def test_credit_card_payment_success_py02(self, setup_payment):
        """
        TC: PY_02 - Verify successful credit card payment
        """
        payment_page = setup_payment
        
        # Select credit card payment
        payment_page.select_payment_method("credit_card")
        
        # Fill card details
        card_details = {
            "number": "4542 9931 9292 2293",
            "expiry_month": "01",
            "expiry_year": "16",
            "cvv": "123",
            "name": "Test User"
        }
        payment_page.fill_credit_card_details(card_details)
        
        # Select country
        payment_page.select_country("India")
        
        # Place order
        payment_page.place_order()
        
        # Verify success
        assert payment_page.verify_order_success(), \
            "Order placement failed"
            
    def test_invalid_card_payment_py03(self, setup_payment):
        """
        TC: PY_03 - Verify payment failure with invalid card
        """
        payment_page = setup_payment
        
        # Fill invalid card details
        card_details = {
            "number": "1111 1111 1111 1111",
            "expiry_month": "01",
            "expiry_year": "16",
            "cvv": "123",
            "name": "Test User"
        }
        payment_page.fill_credit_card_details(card_details)
        payment_page.select_country("India")
        payment_page.place_order()
        
        # Verify error message
        assert payment_page.get_toast_message() == TestData.MESSAGES["payment"]["invalid_card"], \
            "Invalid card error message not shown"
            
    def test_coupon_application_py04(self, setup_payment):
        """
        TC: PY_04 - Verify coupon code application
        """
        payment_page = setup_payment
        
        # Apply valid coupon
        success = payment_page.apply_coupon(TestData.VALID_COUPON)
        assert success, "Coupon application failed"
        
        # Verify price reduction
        assert "discount" in payment_page.get_toast_message().lower(), \
            "Discount not applied after coupon"
            
    def test_country_selection_py05(self, setup_payment):
        """
        TC: PY_05 - Verify country selection functionality
        """
        payment_page = setup_payment
        
        # Select country
        test_country = "India"
        payment_page.select_country(test_country)
        
        # Verify selection
        country_input = payment_page.wait_and_find_element(
            payment_page.COUNTRY_INPUT
        )
        assert test_country in country_input.get_attribute("value"), \
            "Country selection failed"
            
    @pytest.mark.parametrize("payment_method", ["credit_card", "paypal"])
    def test_payment_method_selection_py06(self, setup_payment, payment_method):
        """
        TC: PY_06 - Verify payment method selection
        """
        payment_page = setup_payment
        
        # Select payment method
        payment_page.select_payment_method(payment_method)
        
        # Verify selection
        if payment_method == "credit_card":
            assert "active" in payment_page.wait_and_find_element(
                payment_page.CREDIT_CARD_OPTION
            ).get_attribute("class"), "Credit card not selected"
        else:
            assert "active" in payment_page.wait_and_find_element(
                payment_page.PAYPAL_OPTION
            ).get_attribute("class"), "PayPal not selected"
            
    def test_email_display_py07(self, setup_payment):
        """
        TC: PY_07 - Verify correct email display
        """
        payment_page = setup_payment
        
        # Verify displayed email
        displayed_email = payment_page.get_email_address()
        assert displayed_email == TestData.VALID_USER["email"], \
            f"Wrong email displayed: {displayed_email}"
            
    def test_missing_country_py08(self, setup_payment):
        """
        TC: PY_08 - Verify country validation
        """
        payment_page = setup_payment
        
        # Fill card details but skip country
        card_details = TestData.PAYMENT_METHODS["credit_card"]
        payment_page.fill_credit_card_details(card_details)
        
        # Try to place order
        payment_page.place_order()
        
        # Verify error message
        assert "country" in payment_page.get_toast_message().lower(), \
            "Missing country validation failed"
            
    def test_card_fields_validation_py09(self, setup_payment):
        """
        TC: PY_09 - Verify credit card field validation
        """
        payment_page = setup_payment
        
        # Test with incomplete card number
        card_details = {
            "number": "4111",  # Incomplete
            "expiry_month": "01",
            "expiry_year": "16",
            "cvv": "123",
            "name": "Test User"
        }
        payment_page.fill_credit_card_details(card_details)
        payment_page.select_country("India")
        payment_page.place_order()
        
        # Verify validation message
        assert "card number" in payment_page.get_toast_message().lower(), \
            "Card number validation failed"
            
    def test_order_confirmation_py10(self, setup_payment):
        """
        TC: PY_10 - Verify order confirmation after successful payment
        """
        payment_page = setup_payment
        
        # Complete payment process
        payment_page.select_payment_method("credit_card")
        payment_page.fill_credit_card_details(TestData.PAYMENT_METHODS["credit_card"])
        payment_page.select_country("India")
        payment_page.place_order()
        
        # Verify order confirmation
        assert payment_page.verify_order_success(), \
            "Order confirmation not displayed"
        assert "order" in payment_page.driver.current_url.lower(), \
            "Not redirected to order confirmation page"