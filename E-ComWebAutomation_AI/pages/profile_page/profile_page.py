from selenium.webdriver.common.by import By
from ..base_page import BasePage

class ProfilePage(BasePage):
    """
    Page Object Model for User Profile Management.
    Handles user profile updates and order history.
    """
    # Profile Information
    PROFILE_NAME_INPUT = (By.CSS_SELECTOR, "input[formcontrolname='name']")
    EMAIL_DISPLAY = (By.CSS_SELECTOR, ".email-display")
    ADDRESS_TEXTAREA = (By.CSS_SELECTOR, "textarea[formcontrolname='address']")
    PHONE_INPUT = (By.CSS_SELECTOR, "input[formcontrolname='phone']")
    SAVE_BUTTON = (By.CSS_SELECTOR, "button.btn-save")
    
    # Order History Section
    ORDERS_TAB = (By.CSS_SELECTOR, "button.orders-tab")
    ORDER_ITEMS = (By.CSS_SELECTOR, ".order-card")
    ORDER_ID = (By.CSS_SELECTOR, ".order-id")
    ORDER_DATE = (By.CSS_SELECTOR, ".order-date")
    ORDER_STATUS = (By.CSS_SELECTOR, ".order-status")
    ORDER_TOTAL = (By.CSS_SELECTOR, ".order-total")
    
    # Address Management
    ADD_ADDRESS_BTN = (By.CSS_SELECTOR, "button.add-address")
    ADDRESS_LIST = (By.CSS_SELECTOR, ".address-list .address-item")
    EDIT_ADDRESS_BTN = (By.CSS_SELECTOR, ".edit-address")
    DELETE_ADDRESS_BTN = (By.CSS_SELECTOR, ".delete-address")
    
    def update_profile(self, name=None, address=None, phone=None):
        """
        Update profile information.
        Args:
            name (str, optional): New name
            address (str, optional): New address
            phone (str, optional): New phone number
        Returns:
            bool: True if update was successful
        """
        if name:
            self.fill_input(self.PROFILE_NAME_INPUT, name)
        if address:
            self.fill_input(self.ADDRESS_TEXTAREA, address)
        if phone:
            self.fill_input(self.PHONE_INPUT, phone)
            
        self.wait_and_click(self.SAVE_BUTTON)
        return self.is_toast_message_present()
    
    def get_profile_details(self):
        """
        Get current profile information.
        Returns:
            dict: Profile details
        """
        return {
            "name": self.wait_and_find_element(self.PROFILE_NAME_INPUT).get_attribute("value"),
            "email": self.wait_and_find_element(self.EMAIL_DISPLAY).text,
            "address": self.wait_and_find_element(self.ADDRESS_TEXTAREA).get_attribute("value"),
            "phone": self.wait_and_find_element(self.PHONE_INPUT).get_attribute("value")
        }
    
    def view_order_history(self):
        """
        Switch to order history tab and get order details.
        Returns:
            list: List of order dictionaries
        """
        self.wait_and_click(self.ORDERS_TAB)
        orders = []
        
        order_elements = self.driver.find_elements(*self.ORDER_ITEMS)
        for order in order_elements:
            orders.append({
                "id": order.find_element(*self.ORDER_ID).text,
                "date": order.find_element(*self.ORDER_DATE).text,
                "status": order.find_element(*self.ORDER_STATUS).text,
                "total": order.find_element(*self.ORDER_TOTAL).text
            })
        return orders
    
    def add_new_address(self, address_details):
        """
        Add a new shipping address.
        Args:
            address_details (dict): Address information
        Returns:
            bool: True if address was added successfully
        """
        self.wait_and_click(self.ADD_ADDRESS_BTN)
        for field, value in address_details.items():
            input_locator = (By.CSS_SELECTOR, f"input[formcontrolname='{field}']")
            self.fill_input(input_locator, value)
            
        self.wait_and_click(self.SAVE_BUTTON)
        return self.is_toast_message_present()
    
    def get_saved_addresses(self):
        """
        Get list of saved addresses.
        Returns:
            list: List of address dictionaries
        """
        addresses = []
        address_elements = self.driver.find_elements(*self.ADDRESS_LIST)
        
        for addr in address_elements:
            addresses.append({
                "text": addr.text,
                "is_default": "default" in addr.get_attribute("class").lower()
            })
        return addresses
    
    def delete_address(self, index):
        """
        Delete an address by its index.
        Args:
            index (int): Index of address to delete
        Returns:
            bool: True if deletion was successful
        """
        addresses = self.driver.find_elements(*self.ADDRESS_LIST)
        if 0 <= index < len(addresses):
            delete_btn = addresses[index].find_element(*self.DELETE_ADDRESS_BTN)
            delete_btn.click()
            return self.is_toast_message_present()
        return False