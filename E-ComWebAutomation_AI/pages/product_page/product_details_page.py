from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from ..base_page import BasePage

class ProductDetailsPage(BasePage):
    """
    Page Object Model for Product Details Page.
    Handles product information, image zoom, and reviews.
    """
    # Product Information
    PRODUCT_TITLE = (By.CSS_SELECTOR, ".product-title")
    PRODUCT_PRICE = (By.CSS_SELECTOR, ".product-price")
    PRODUCT_DESCRIPTION = (By.CSS_SELECTOR, ".product-description")
    PRODUCT_CATEGORY = (By.CSS_SELECTOR, ".product-category")
    
    # Product Images
    MAIN_IMAGE = (By.CSS_SELECTOR, ".main-image")
    THUMBNAIL_IMAGES = (By.CSS_SELECTOR, ".thumbnail-image")
    ZOOM_VIEW = (By.CSS_SELECTOR, ".zoom-view")
    
    # Size Chart
    SIZE_CHART_BTN = (By.CSS_SELECTOR, "button[data-target='#sizeChart']")
    SIZE_CHART_MODAL = (By.ID, "sizeChart")
    SIZE_OPTIONS = (By.CSS_SELECTOR, ".size-option")
    
    # Reviews Section
    REVIEWS_TAB = (By.CSS_SELECTOR, ".reviews-tab")
    REVIEW_LIST = (By.CSS_SELECTOR, ".review-item")
    REVIEW_RATING = (By.CSS_SELECTOR, ".review-rating")
    REVIEW_TEXT = (By.CSS_SELECTOR, ".review-text")
    REVIEW_AUTHOR = (By.CSS_SELECTOR, ".review-author")
    
    # Add Review Form
    ADD_REVIEW_BTN = (By.CSS_SELECTOR, ".add-review-btn")
    RATING_STARS = (By.CSS_SELECTOR, ".rating-star")
    REVIEW_TEXT_INPUT = (By.CSS_SELECTOR, "textarea[formcontrolname='review']")
    SUBMIT_REVIEW_BTN = (By.CSS_SELECTOR, "button[type='submit']")
    
    def get_product_details(self):
        """
        Get all product details.
        Returns:
            dict: Product information
        """
        return {
            "title": self.wait_and_find_element(self.PRODUCT_TITLE).text,
            "price": self.wait_and_find_element(self.PRODUCT_PRICE).text,
            "description": self.wait_and_find_element(self.PRODUCT_DESCRIPTION).text,
            "category": self.wait_and_find_element(self.PRODUCT_CATEGORY).text
        }
    
    def zoom_image(self):
        """
        Trigger image zoom functionality.
        Returns:
            bool: True if zoom view is displayed
        """
        main_image = self.wait_and_find_element(self.MAIN_IMAGE)
        actions = ActionChains(self.driver)
        actions.move_to_element(main_image).perform()
        
        return self.wait_and_find_element(self.ZOOM_VIEW).is_displayed()
    
    def switch_thumbnail(self, index):
        """
        Switch to different product image.
        Args:
            index (int): Index of thumbnail to select
        Returns:
            bool: True if thumbnail was selected
        """
        thumbnails = self.driver.find_elements(*self.THUMBNAIL_IMAGES)
        if 0 <= index < len(thumbnails):
            thumbnails[index].click()
            return True
        return False
    
    def open_size_chart(self):
        """
        Open the size chart modal.
        Returns:
            bool: True if size chart is displayed
        """
        self.wait_and_click(self.SIZE_CHART_BTN)
        size_chart = self.wait_and_find_element(self.SIZE_CHART_MODAL)
        return size_chart.is_displayed()
    
    def select_size(self, size):
        """
        Select a product size.
        Args:
            size (str): Size to select
        Returns:
            bool: True if size was selected
        """
        size_options = self.driver.find_elements(*self.SIZE_OPTIONS)
        for option in size_options:
            if option.text.strip().lower() == size.lower():
                option.click()
                return True
        return False
    
    def view_reviews(self):
        """
        Switch to reviews tab and get all reviews.
        Returns:
            list: List of review dictionaries
        """
        self.wait_and_click(self.REVIEWS_TAB)
        reviews = []
        
        review_elements = self.driver.find_elements(*self.REVIEW_LIST)
        for review in review_elements:
            reviews.append({
                "rating": len(review.find_elements(By.CSS_SELECTOR, ".star-filled")),
                "text": review.find_element(*self.REVIEW_TEXT).text,
                "author": review.find_element(*self.REVIEW_AUTHOR).text
            })
        return reviews
    
    def add_review(self, rating, text):
        """
        Add a new product review.
        Args:
            rating (int): Star rating (1-5)
            text (str): Review text
        Returns:
            bool: True if review was submitted successfully
        """
        self.wait_and_click(self.ADD_REVIEW_BTN)
        
        # Select rating
        rating_stars = self.driver.find_elements(*self.RATING_STARS)
        if 1 <= rating <= len(rating_stars):
            rating_stars[rating - 1].click()
        
        # Add review text
        self.fill_input(self.REVIEW_TEXT_INPUT, text)
        
        # Submit review
        self.wait_and_click(self.SUBMIT_REVIEW_BTN)
        return self.is_toast_message_present()