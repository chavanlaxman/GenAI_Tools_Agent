from selenium.webdriver.common.by import By
from ..base_page import BasePage


class CartPage(BasePage):
    """
    Page Object Model for the Shopping Cart and Checkout functionality.
    Handles test cases CO_01 through CO_08.
    """
    # --- Header Elements ---
    CART_TITLE = (By.CSS_SELECTOR, "h1")
    CONTINUE_SHOPPING_BTN = (By.CSS_SELECTOR, "button[routerlink='/dashboard']")
    
    # --- Cart Item Elements ---
    CART_ITEMS = (By.CSS_SELECTOR, ".cartWrap .items")
    ITEM_IMAGE = (By.CSS_SELECTOR, ".itemImg")
    ITEM_NUMBER = (By.CSS_SELECTOR, ".itemNumber")
    ITEM_TITLE = (By.CSS_SELECTOR, "h3")
    ITEM_PRICE = (By.CSS_SELECTOR, ".cartSection p:nth-child(4)")  # MRP price
    ITEM_STOCK_STATUS = (By.CSS_SELECTOR, ".stockStatus")
    
    # --- Item Actions ---
    BUY_NOW_BTN = (By.CSS_SELECTOR, ".cartSection .btn-primary")
    REMOVE_ITEM_BTN = (By.CSS_SELECTOR, ".cartSection .btn-danger")
    ITEM_QTY_INPUT = (By.CSS_SELECTOR, ".cartSection input[type='number'], .cartSection .qty")
    
    # --- Order Summary ---
    SUBTOTAL_VALUE = (By.CSS_SELECTOR, ".totalRow:nth-child(1) .value")
    TOTAL_VALUE = (By.CSS_SELECTOR, ".totalRow:nth-child(2) .value")
    CHECKOUT_BTN = (By.CSS_SELECTOR, ".totalRow .btn-primary")
    
    # --- Cart Status ---
    CART_COUNT = (By.CSS_SELECTOR, ".fa-shopping-cart + label")
    
    def get_cart_title(self):
        """Get the cart page title text."""
        return self.wait_and_find_element(self.CART_TITLE).text
    
    def continue_shopping(self):
        """Click continue shopping button to return to dashboard."""
        self.wait_and_click(self.CONTINUE_SHOPPING_BTN)
        
    def get_cart_items(self):
        """
        Get details of all items in cart.
        Returns:
            list: List of dictionaries containing item details
        """
        items = []
        cart_items = self.driver.find_elements(*self.CART_ITEMS)
        
        for item in cart_items:
            item_data = {
                "number": item.find_element(By.CSS_SELECTOR, ".itemNumber").text.replace("#", ""),
                "title": item.find_element(By.CSS_SELECTOR, "h3").text,
                "price": item.find_element(By.CSS_SELECTOR, ".cartSection p:contains('MRP')").text
                    .replace("MRP $", "").strip(),
                "stock_status": item.find_element(By.CSS_SELECTOR, ".stockStatus").text,
                "total": item.find_element(By.CSS_SELECTOR, ".prodTotal p").text
                    .replace("$", "").strip()
            }
            items.append(item_data)
        return items
    
    def get_cart_count(self):
        """Get the number of items in cart from header badge."""
        try:
            count = self.wait_and_find_element(self.CART_COUNT).text
            return int(count)
        except:
            return 0
            
    def remove_item(self, item_title):
        """
        Remove a specific item from cart.
        Args:
            item_title (str): Title of item to remove
        Returns:
            bool: True if item was removed
        """
        cart_items = self.driver.find_elements(*self.CART_ITEMS)
        for item in cart_items:
            if item.find_element(By.CSS_SELECTOR, "h3").text == item_title:
                item.find_element(By.CSS_SELECTOR, ".btn-danger").click()
                return True
        return False
        
    def buy_now(self, item_title):
        """
        Click Buy Now for a specific item.
        Args:
            item_title (str): Title of item to buy
        Returns:
            bool: True if Buy Now was clicked
        """
        cart_items = self.driver.find_elements(*self.CART_ITEMS)
        for item in cart_items:
            if item.find_element(By.CSS_SELECTOR, "h3").text == item_title:
                item.find_element(By.CSS_SELECTOR, ".btn-primary").click()
                return True
        return False
        
    def get_subtotal(self):
        """Get cart subtotal value."""
        subtotal = self.wait_and_find_element(self.SUBTOTAL_VALUE).text
        return float(subtotal.replace("$", "").strip())
        
    def get_total(self):
        """Get cart total value."""
        total = self.wait_and_find_element(self.TOTAL_VALUE).text
        return float(total.replace("$", "").strip())
        
    def proceed_to_checkout(self):
        """Click the checkout button."""
        self.wait_and_click(self.CHECKOUT_BTN)
        
    def is_cart_empty(self):
        """Check if cart is empty."""
        return len(self.driver.find_elements(*self.CART_ITEMS)) == 0
        
    def verify_item_in_cart(self, expected_item):
        """
        Verify if an item exists in cart with expected details.
        Args:
            expected_item (dict): Expected item details
        Returns:
            bool: True if item matches expectations
        """
        items = self.get_cart_items()
        for item in items:
            if (item["title"] == expected_item["title"] and 
                item["price"] == expected_item["price"]):
                return True
        return False

    def update_item_quantity(self, item_title, quantity):
        """
        Update quantity for a specific item in cart.
        Args:
            item_title (str): Title of item to update
            quantity (int): Desired quantity
        Returns:
            bool: True if update succeeded
        """
        cart_items = self.driver.find_elements(*self.CART_ITEMS)
        for item in cart_items:
            try:
                title = item.find_element(By.CSS_SELECTOR, "h3").text
            except:
                title = ""
            if title == item_title:
                # Try number input first
                try:
                    qty_input = item.find_element(By.CSS_SELECTOR, "input[type='number']")
                    qty_input.clear()
                    qty_input.send_keys(str(quantity))
                    # trigger update if there's an update button
                    try:
                        item.find_element(By.CSS_SELECTOR, ".update-qty, button.update").click()
                    except:
                        pass
                    return True
                except:
                    # fallback: try dropdowns or other controls
                    try:
                        select = item.find_element(By.CSS_SELECTOR, "select.qty")
                        for opt in select.find_elements(By.TAG_NAME, 'option'):
                            if opt.text.strip() == str(quantity):
                                opt.click()
                                return True
                    except:
                        return False
        return False