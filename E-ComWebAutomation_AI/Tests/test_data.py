"""Test data configuration for all test cases."""
import os
from datetime import datetime


class TestData:
    """
    Central configuration for test data.
    Update this class when test data needs to change.
    """
    # Environment variables (can be overridden by env vars)
    BASE_URL = os.getenv('TEST_BASE_URL', 'https://rahulshettyacademy.com/client/#/auth/login')
    ADMIN_EMAIL = os.getenv('TEST_ADMIN_EMAIL', 'admin@example.com')
    
    # User credentials
    VALID_USER = {
        "email": "test.qa@shop.com",
        "password": "ValidPassword123!",
        "name": "Test User"
    }
    
    INVALID_USER = {
        "email": "invalid@shop.com",
        "password": "WrongPassword456",
        "name": "Invalid User"
    }

    # Product data
    PRODUCTS = {
        "zara_coat": {
            "title": "ZARA COAT 3",
            "price": "11500",
            "category": "fashion",
            "subcategory": "t-shirts"
        },
        "adidas": {
            "title": "ADIDAS ORIGINAL",
            "price": "11500",
            "category": "fashion",
            "subcategory": "shoes"
        },
        "iphone": {
            "title": "iphone 13 pro",
            "price": "55000",
            "category": "electronics",
            "subcategory": "mobiles"
        }
    }

    # Filter combinations
    PRICE_RANGES = [
        {"min": "1000", "max": "5000", "expected_count": 0},
        {"min": "10000", "max": "20000", "expected_count": 2},
        {"min": "50000", "max": "60000", "expected_count": 1}
    ]

    # Categories and subcategories
    CATEGORIES = ["fashion", "electronics", "household"]
    SUBCATEGORIES = {
        "fashion": ["t-shirts", "shirts", "shoes"],
        "electronics": ["mobiles", "laptops"],
    }

    @staticmethod
    def generate_unique_email(prefix="testuser"):
        """Generate a unique email using timestamp."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{prefix}_{timestamp}@gauto.com"

    @staticmethod
    def get_valid_password():
        """Returns a valid password meeting security requirements."""
        return "Test@123456"  # Meets common password requirements

    # Cart test data
    CART_ITEMS = {
        "single_item": {
            "product": "ZARA COAT 3",
            "expected_total": "11500"
        },
        "multiple_items": {
            "products": ["ZARA COAT 3", "ADIDAS ORIGINAL"],
            "expected_total": "23000"
        }
    }
    
    # Checkout test data
    SHIPPING_ADDRESS = {
        "street": "123 Test Street",
        "city": "Test City",
        "state": "Test State",
        "zip": "12345",
        "country": "Test Country"
    }
    
    PAYMENT_METHODS = {
        "credit_card": {
            "type": "VISA",
            "number": "4111111111111111",
            "expiry": "12/25",
            "cvv": "123"
        },
        "debit_card": {
            "type": "Mastercard",
            "number": "5555555555554444",
            "expiry": "12/25",
            "cvv": "123"
        }
    }

    # Error messages and extra test data
    # Valid coupon code for testing
    VALID_COUPON = "DISCOUNT20"

    # Forgot password test email
    FORGOT_EMAIL = "recover_me@gauto.com"

    # Social providers available for social login tests (smoke checks)
    SOCIAL_PROVIDERS = ["google", "facebook"]

    # Expected recommendations mapping (used by PC_08)
    RECOMMENDATIONS = {
        "fashion": ["ZARA COAT 3", "ADIDAS ORIGINAL"],
        "electronics": ["iphone 13 pro"]
    }

    MESSAGES = {
        "login": {
            "invalid_credentials": "Invalid email or password",
            "success": "Login Successfully"
        },
        "registration": {
            "success": "Registration Successfully",
            "email_exists": "Email already registered",
            "password_mismatch": "Passwords do not match"
        },
        "cart": {
            "added": "Product Added To Cart",
            "removed": "Product Removed from Cart",
            "empty": "No Products in Your Cart",
            "max_quantity": "Maximum quantity limit reached",
            "out_of_stock": "Product is out of stock"
        },
        "checkout": {
            "success": "Order placed successfully",
            "address_required": "Shipping address is required",
            "payment_failed": "Payment processing failed",
            "invalid_card": "Invalid card details"
        },
        "payment": {
            "success": "Payment successful",
            "invalid_card": "Invalid card details",
            "card_declined": "Card was declined",
            "missing_fields": "Please fill all required fields",
            "country_required": "Please select a country",
            "coupon_applied": "Discount applied successfully",
            "invalid_coupon": "Invalid coupon code",
            "order_confirmed": "Order placed successfully"
        }
    }