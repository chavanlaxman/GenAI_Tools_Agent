import pytest
from pages.profile_page.profile_page import ProfilePage
from pages.login_page.login import LoginPage
from .test_data import TestData


@pytest.fixture
def setup_profile(driver_for_test):
    """
    Fixture that provides a logged-in session with profile page access.
    Returns profile page object.
    """
    # Login first
    login_page = LoginPage(driver_for_test)
    login_page.perform_login(
        TestData.VALID_USER["email"],
        TestData.VALID_USER["password"]
    )
    
    return ProfilePage(driver_for_test)


class TestProfile:
    """
    Test suite for Profile Management functionality.
    Covers test cases UA_07 and UA_08.
    """
    
    def test_profile_update_ua07(self, setup_profile):
        """
        TC: UA_07 - Verify profile update functionality
        """
        profile_page = setup_profile
        
        # Update profile information
        new_details = {
            "name": "Updated Name",
            "address": "123 New Street, City, Country",
            "phone": "1234567890"
        }
        
        success = profile_page.update_profile(
            name=new_details["name"],
            address=new_details["address"],
            phone=new_details["phone"]
        )
        
        # Verify update success
        assert success, "Profile update failed"
        
        # Verify updated details
        current_details = profile_page.get_profile_details()
        assert current_details["name"] == new_details["name"], "Name update failed"
        assert current_details["address"] == new_details["address"], "Address update failed"
        assert current_details["phone"] == new_details["phone"], "Phone update failed"
    
    def test_order_history_ua08(self, setup_profile):
        """
        TC: UA_08 - Verify order history display
        """
        profile_page = setup_profile
        
        # View order history
        orders = profile_page.view_order_history()
        
        # Verify orders are displayed
        assert len(orders) > 0, "No orders found in history"
        
        # Verify order details structure
        for order in orders:
            assert all(key in order for key in ["id", "date", "status", "total"]), \
                "Order details incomplete"
    
    def test_add_new_address(self, setup_profile):
        """
        Verify adding new shipping address
        """
        profile_page = setup_profile
        
        # Add new address
        new_address = {
            "street": "456 Test Ave",
            "city": "Test City",
            "state": "Test State",
            "zip": "12345",
            "country": "Test Country"
        }
        
        success = profile_page.add_new_address(new_address)
        assert success, "Failed to add new address"
        
        # Verify address was added
        addresses = profile_page.get_saved_addresses()
        assert any(new_address["street"] in addr["text"] for addr in addresses), \
            "New address not found in saved addresses"
    
    def test_delete_address(self, setup_profile):
        """
        Verify address deletion functionality
        """
        profile_page = setup_profile
        
        # Get initial address count
        initial_addresses = profile_page.get_saved_addresses()
        if not initial_addresses:
            pytest.skip("No addresses available to delete")
        
        # Delete first address
        success = profile_page.delete_address(0)
        assert success, "Address deletion failed"
        
        # Verify address was deleted
        current_addresses = profile_page.get_saved_addresses()
        assert len(current_addresses) == len(initial_addresses) - 1, \
            "Address count didn't decrease after deletion"
    
    def test_address_validation(self, setup_profile):
        """
        Verify address form validation
        """
        profile_page = setup_profile
        
        # Try to add address with missing fields
        incomplete_address = {
            "street": "123 Test St",
            # Missing other required fields
        }
        
        profile_page.add_new_address(incomplete_address)
        
        # Verify error message
        assert "required" in profile_page.get_toast_message().lower(), \
            "Missing field validation failed"
    
    def test_multiple_addresses(self, setup_profile):
        """
        Verify multiple address management
        """
        profile_page = setup_profile
        
        # Add multiple addresses
        addresses = [
            {
                "street": f"{i} Test Street",
                "city": "Test City",
                "state": "Test State",
                "zip": f"1234{i}",
                "country": "Test Country"
            }
            for i in range(3)
        ]
        
        for addr in addresses:
            success = profile_page.add_new_address(addr)
            assert success, f"Failed to add address: {addr['street']}"
        
        # Verify all addresses were added
        saved_addresses = profile_page.get_saved_addresses()
        assert len(saved_addresses) >= len(addresses), \
            "Not all addresses were saved"