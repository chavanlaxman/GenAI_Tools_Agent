from selenium.webdriver.common.by import By
from ..base_page import BasePage

class PaymentPage(BasePage):
    """
    Page Object Model for Payment and Order Placement page.
    Handles credit card payment and order submission functionality.
    """
    # Product Details Section
    PRODUCT_IMAGE = (By.CSS_SELECTOR, "img.iphone")
    PRODUCT_TITLE = (By.CSS_SELECTOR, ".item__title")
    PRODUCT_PRICE = (By.CSS_SELECTOR, ".item__price")
    PRODUCT_QUANTITY = (By.CSS_SELECTOR, ".item__quantity")
    PRODUCT_DESCRIPTION = (By.CSS_SELECTOR, ".item__description ul li")

    # Payment Method Selection
    CREDIT_CARD_OPTION = (By.CSS_SELECTOR, ".payment__type--cc")
    PAYPAL_OPTION = (By.CSS_SELECTOR, ".payment__type--paypal")
    
    # Credit Card Form Fields
    CARD_NUMBER_INPUT = (By.CSS_SELECTOR, ".form__cc input[type='text']")
    EXPIRY_MONTH_SELECT = (By.CSS_SELECTOR, ".form__cc select:first-of-type")
    EXPIRY_YEAR_SELECT = (By.CSS_SELECTOR, ".form__cc select:last-of-type")
    CVV_INPUT = (By.CSS_SELECTOR, "input.txt[type='text']")
    NAME_ON_CARD_INPUT = (By.CSS_SELECTOR, ".form__cc .row:nth-child(3) input")
    
    # Coupon Section
    COUPON_CODE_INPUT = (By.NAME, "coupon")
    APPLY_COUPON_BTN = (By.CSS_SELECTOR, "button[type='submit']")
    
    # Shipping Information
    EMAIL_DISPLAY = (By.CSS_SELECTOR, "label[type='text']")
    COUNTRY_INPUT = (By.CSS_SELECTOR, "input[placeholder='Select Country']")
    COUNTRY_OPTIONS = (By.CSS_SELECTOR, "ngx-typeahead-item")
    
    # Order Placement
    PLACE_ORDER_BTN = (By.CSS_SELECTOR, "a.action__submit")

    def verify_product_details(self, expected_product):
        """
        Verify the displayed product details match expected values.
        Args:
            expected_product (dict): Expected product details
        Returns:
            bool: True if all details match
        """
        actual_title = self.wait_and_find_element(self.PRODUCT_TITLE).text.strip()
        actual_price = self.wait_and_find_element(self.PRODUCT_PRICE).text.strip()
        actual_quantity = self.wait_and_find_element(self.PRODUCT_QUANTITY).text.strip()
        
        return (
            actual_title == expected_product["title"] and
            actual_price == f"$ {expected_product['price']}" and
            actual_quantity == f"Quantity: {expected_product['quantity']}"
        )

    def select_payment_method(self, method="credit_card"):
        """
        Select the payment method.
        Args:
            method (str): Payment method to select (credit_card, paypal)
        """
        if method == "credit_card":
            self.wait_and_click(self.CREDIT_CARD_OPTION)
        elif method == "paypal":
            self.wait_and_click(self.PAYPAL_OPTION)

    def fill_credit_card_details(self, card_details):
        """
        Fill credit card payment details.
        Args:
            card_details (dict): Card information including number, expiry, cvv, name
        """
        self.fill_input(self.CARD_NUMBER_INPUT, card_details["number"])
        self.select_dropdown(self.EXPIRY_MONTH_SELECT, card_details["expiry_month"])
        self.select_dropdown(self.EXPIRY_YEAR_SELECT, card_details["expiry_year"])
        self.fill_input(self.CVV_INPUT, card_details["cvv"])
        self.fill_input(self.NAME_ON_CARD_INPUT, card_details["name"])

    def apply_coupon(self, coupon_code):
        """
        Apply a coupon code.
        Args:
            coupon_code (str): Coupon code to apply
        Returns:
            bool: True if coupon was successfully applied
        """
        self.fill_input(self.COUPON_CODE_INPUT, coupon_code)
        self.wait_and_click(self.APPLY_COUPON_BTN)
        return self.is_toast_message_present()

    def select_country(self, country_name):
        """
        Select shipping country.
        Args:
            country_name (str): Country to select
        """
        country_input = self.wait_and_find_element(self.COUNTRY_INPUT)
        country_input.clear()
        country_input.send_keys(country_name)
        
        # Wait for and select country from dropdown
        country_options = self.wait.until(
            EC.presence_of_all_elements_located(self.COUNTRY_OPTIONS)
        )
        for option in country_options:
            if country_name.lower() in option.text.lower():
                option.click()
                break

    def get_email_address(self):
        """Get the displayed email address."""
        return self.wait_and_find_element(self.EMAIL_DISPLAY).text.strip()

    def place_order(self):
        """
        Click the place order button.
        Returns:
            bool: True if order was placed successfully
        """
        self.wait_and_click(self.PLACE_ORDER_BTN)
        return self.is_toast_message_present()

    def verify_order_success(self):
        """
        Verify order was placed successfully.
        Returns:
            bool: True if success message is present
        """
        return "thankyou" in self.driver.current_url.lower()