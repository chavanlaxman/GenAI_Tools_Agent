from selenium.webdriver.common.by import By
from ..base_page import BasePage


class DashboardPage(BasePage):
    """
    Page Object Model for the E-commerce Dashboard Page.
    Handles product listing, filtering, and cart operations.
    """
    # --- Navigation Elements ---
    HOME_BUTTON = (By.CSS_SELECTOR, "button.btn-custom i.fa-home")
    ORDERS_BUTTON = (By.CSS_SELECTOR, "button.btn-custom i.fa-handshake-o")
    CART_BUTTON = (By.CSS_SELECTOR, "button.btn-custom i.fa-shopping-cart")
    SIGN_OUT_BUTTON = (By.CSS_SELECTOR, "button.btn-custom i.fa-sign-out")
    
    # --- Filter Elements ---
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[formcontrolname='productName']")
    MIN_PRICE_INPUT = (By.CSS_SELECTOR, "input[formcontrolname='minPrice']")
    MAX_PRICE_INPUT = (By.CSS_SELECTOR, "input[formcontrolname='maxPrice']")
    
    # Category checkboxes
    CATEGORY_FASHION = (By.XPATH, "//label[text()='fashion']/preceding-sibling::input")
    CATEGORY_ELECTRONICS = (By.XPATH, "//label[text()='electronics']/preceding-sibling::input")
    CATEGORY_HOUSEHOLD = (By.XPATH, "//label[text()='household']/preceding-sibling::input")
    
    # Subcategory checkboxes
    SUBCATEGORY_MAP = {
        "t-shirts": "//label[text()='t-shirts']/preceding-sibling::input",
        "shirts": "//label[text()='shirts']/preceding-sibling::input",
        "shoes": "//label[text()='shoes']/preceding-sibling::input",
        "mobiles": "//label[text()='mobiles']/preceding-sibling::input",
        "laptops": "//label[text()='laptops']/preceding-sibling::input"
    }
    
    # --- Product Elements ---
    PRODUCT_CARDS = (By.CSS_SELECTOR, ".card")
    PRODUCT_TITLES = (By.CSS_SELECTOR, ".card-body h5 b")
    PRODUCT_PRICES = (By.CSS_SELECTOR, ".card-body .text-muted")
    VIEW_BUTTONS = (By.CSS_SELECTOR, "button.btn i.fa-eye")
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, "button.btn i.fa-shopping-cart")
    
    # --- Results Info ---
    RESULTS_COUNT = (By.CSS_SELECTOR, "#res")
    
    def navigate_to_orders(self):
        """Navigate to the orders page."""
        self.wait_and_click(self.ORDERS_BUTTON)
        
    def navigate_to_cart(self):
        """Navigate to the shopping cart."""
        self.wait_and_click(self.CART_BUTTON)
        
    def sign_out(self):
        """Sign out from the application."""
        self.wait_and_click(self.SIGN_OUT_BUTTON)
        
    def search_products(self, keyword):
        """
        Search for products using the search input.
        Args:
            keyword (str): Search term
        """
        self.fill_input(self.SEARCH_INPUT, keyword)
        
    def set_price_range(self, min_price, max_price):
        """
        Set the price range filter.
        Args:
            min_price (str): Minimum price
            max_price (str): Maximum price
        """
        if min_price:
            self.fill_input(self.MIN_PRICE_INPUT, min_price)
        if max_price:
            self.fill_input(self.MAX_PRICE_INPUT, max_price)
            
    def select_category(self, category_name):
        """
        Select a main category.
        Args:
            category_name (str): Category to select (fashion/electronics/household)
        """
        category_map = {
            "fashion": self.CATEGORY_FASHION,
            "electronics": self.CATEGORY_ELECTRONICS,
            "household": self.CATEGORY_HOUSEHOLD
        }
        if category_name.lower() in category_map:
            self.wait_and_click(category_map[category_name.lower()])
            
    def select_subcategory(self, subcategory_name):
        """
        Select a subcategory.
        Args:
            subcategory_name (str): Subcategory to select
        """
        if subcategory_name.lower() in self.SUBCATEGORY_MAP:
            locator = (By.XPATH, self.SUBCATEGORY_MAP[subcategory_name.lower()])
            self.wait_and_click(locator)
            
    def get_product_count(self):
        """Get the number of products displayed."""
        return len(self.driver.find_elements(*self.PRODUCT_CARDS))
        
    def get_product_details(self):
        """
        Get details of all displayed products.
        Returns:
            list: List of dictionaries containing product details
        """
        products = []
        cards = self.driver.find_elements(*self.PRODUCT_CARDS)
        
        for card in cards:
            title = card.find_element(By.CSS_SELECTOR, "h5 b").text
            price = card.find_element(By.CSS_SELECTOR, ".text-muted").text
            products.append({
                "title": title,
                "price": price.replace("$ ", "")
            })
        return products
        
    def add_product_to_cart(self, product_title):
        """
        Add a specific product to cart by its title.
        Args:
            product_title (str): Title of the product to add
        Returns:
            bool: True if product was added successfully
        """
        cards = self.driver.find_elements(*self.PRODUCT_CARDS)
        for card in cards:
            title = card.find_element(By.CSS_SELECTOR, "h5 b").text
            if title.lower() == product_title.lower():
                cart_btn = card.find_element(By.CSS_SELECTOR, "button.btn i.fa-shopping-cart")
                cart_btn.click()
                return True
        return False
        
    def view_product_details(self, product_title):
        """
        Click the view button for a specific product.
        Args:
            product_title (str): Title of the product to view
        Returns:
            bool: True if product was found and viewed
        """
        cards = self.driver.find_elements(*self.PRODUCT_CARDS)
        for card in cards:
            title = card.find_element(By.CSS_SELECTOR, "h5 b").text
            if title.lower() == product_title.lower():
                view_btn = card.find_element(By.CSS_SELECTOR, "button.btn i.fa-eye")
                view_btn.click()
                return True
        return False
        
    def get_results_count_text(self):
        """Get the results count text."""
        return self.wait_and_find_element(self.RESULTS_COUNT).text

    # --- Recommendations ---
    RECOMMENDATIONS_SECTION = (By.CSS_SELECTOR, ".recommended")
    RECOMMENDED_PRODUCT_CARDS = (By.CSS_SELECTOR, ".recommended .card")

    def get_recommendations(self):
        """
        Return list of recommended products shown on dashboard/homepage.
        """
        try:
            cards = self.driver.find_elements(*self.RECOMMENDED_PRODUCT_CARDS)
            recommendations = []
            for c in cards:
                title = c.find_element(By.CSS_SELECTOR, "h5 b").text
                price = c.find_element(By.CSS_SELECTOR, ".text-muted").text
                recommendations.append({"title": title, "price": price.replace('$ ', '')})
            return recommendations
        except Exception:
            return []

    def browse_product_for_recommendation(self, product_title):
        """
        Simulate browsing a product to influence recommendations.
        Opens product details then navigates back to dashboard.
        """
        if self.view_product_details(product_title):
            # assume product details page has a back button or use browser back
            self.driver.back()
            return True
        return False