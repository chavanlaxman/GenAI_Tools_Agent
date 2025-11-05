1. USER ACCOUNT MODULE – Functional Test Cases

3. | TC ID | Test Case Title                             | Steps                                                                                                | Expected Result                                                         | Priority |
| ----- | ------------------------------------------- | ---------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- | -------- |
| UA_01 | Verify user registration with valid data    | 1. Open site <br>2. Click “Sign Up” <br>3. Enter valid name, email, password <br>4. Click “Register” | User account created successfully and redirected to dashboard/home page | High     |
| UA_02 | Verify registration with existing email     | 1. Try registering with an already used email                                                        | System displays “Email already registered” error                        | High     |
| UA_03 | Verify login with valid credentials         | 1. Enter valid email and password <br>2. Click Login                                                 | User logged in and navigated to home page                               | High     |
| UA_04 | Verify login with invalid credentials       | 1. Enter wrong email or password <br>2. Click Login                                                  | Error message shown “Invalid credentials”                               | High     |
| UA_05 | Verify forgot password functionality        | 1. Click “Forgot Password” <br>2. Enter registered email <br>3. Click Submit                         | Password reset link sent to email                                       | Medium   |
| UA_06 | Verify social media login (Google/Facebook) | 1. Click “Login with Google/Facebook” <br>2. Authorize access                                        | User successfully logged in using linked account                        | Medium   |
| UA_07 | Verify profile update                       | 1. Go to Profile <br>2. Edit Name/Address <br>3. Save changes                                        | Profile updates reflected successfully                                  | Medium   |
| UA_08 | Verify order history displays past orders   | 1. Go to “My Orders” <br>2. View past orders                                                         | All past orders displayed with details                                  | Medium   |
| UA_09 | Verify logout functionality                 | 1. Click “Logout” from menu                                                                          | User logged out and redirected to login page                            | Low      |


2. 👗 2. PRODUCT CATALOG MODULE – Functional Test Cases
| TC ID | Test Case Title                            | Steps                                                               | Expected Result                                            | Priority |
| ----- | ------------------------------------------ | ------------------------------------------------------------------- | ---------------------------------------------------------- | -------- |
| PC_01 | Verify browsing by category                | 1. Go to catalog <br>2. Select a category (e.g., Dresses)           | Displays all products under selected category              | High     |
| PC_02 | Verify product search with keyword         | 1. Enter keyword (e.g., “Jacket”) in search bar                     | Matching products displayed                                | High     |
| PC_03 | Verify search with no results              | 1. Search non-existent product                                      | “No products found” message displayed                      | Medium   |
| PC_04 | Verify product filter (size, price, brand) | 1. Apply size or price filter                                       | Product list updates as per applied filters                | High     |
| PC_05 | Verify product detail page display         | 1. Click on any product                                             | Product page shows image, name, price, size chart, reviews | High     |
| PC_06 | Verify image zoom feature                  | 1. Hover or click zoom on image                                     | Product image zooms in clearly                             | Medium   |
| PC_07 | Verify review section                      | 1. Scroll to reviews section <br>2. Add a new review (if logged in) | Review successfully added and displayed                    | Medium   |
| PC_08 | Verify personalized recommendations        | 1. Browse few products <br>2. Go to homepage                        | “Recommended for you” section updated based on browsing    | Low      |

🛒 3. SHOPPING CART MODULE – Functional Test Cases
| TC ID | Test Case Title                     | Steps                                                               | Expected Result                                 | Priority |
| ----- | ----------------------------------- | ------------------------------------------------------------------- | ----------------------------------------------- | -------- |
| SC_01 | Verify adding a product to cart     | 1. Select product <br>2. Click “Add to Cart”                        | Product appears in cart with price and quantity | High     |
| SC_02 | Verify removing product from cart   | 1. Open cart <br>2. Click “Remove” for a product                    | Product successfully removed                    | High     |
| SC_03 | Verify updating product quantity    | 1. Open cart <br>2. Change quantity (e.g., 1 → 3)                   | Quantity and total price updated accordingly    | High     |
| SC_04 | Verify price calculation            | 1. Add multiple items <br>2. Check total amount                     | Total = Sum of all item prices + shipping       | High     |
| SC_05 | Verify empty cart message           | 1. Remove all items from cart                                       | “Your cart is empty” message displayed          | Medium   |
| SC_06 | Verify product availability in cart | 1. Add product <br>2. Product goes out of stock <br>3. Refresh cart | System shows message “Product out of stock”     | Medium   |
| SC_07 | Verify continue shopping button     | 1. Open cart <br>2. Click “Continue Shopping”                       | User redirected back to product listing page    | Low      |

1. CHECKOUT MODULE – Functional Test Cases
| TC ID | Test Case Title                                | Steps                                                                     | Expected Result                                                           | Priority |
| ----- | ---------------------------------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------- | -------- |
| CO_01 | Verify user navigates to checkout from cart    | 1. Add items to cart <br>2. Click “Proceed to Checkout”                   | User redirected to checkout page                                          | High     |
| CO_02 | Verify shipping address selection              | 1. At checkout, choose an existing saved address                          | Address details populated correctly                                       | High     |
| CO_03 | Verify adding new shipping address             | 1. Click “Add New Address” <br>2. Enter valid details <br>3. Save         | New address added and available for selection                             | Medium   |
| CO_04 | Verify multiple shipping methods display       | 1. Proceed to shipping options                                            | Available shipping methods (Standard, Express, etc.) displayed with costs | High     |
| CO_05 | Verify selecting shipping method updates total | 1. Change shipping method                                                 | Order total recalculates based on selected method                         | High     |
| CO_06 | Verify checkout with empty cart                | 1. Navigate to checkout without adding products                           | System shows message “Your cart is empty”                                 | High     |
| CO_07 | Verify back navigation to cart                 | 1. On checkout page, click “Back to Cart”                                 | User returned to cart page without data loss                              | Medium   |
| CO_08 | Verify order summary details                   | 1. Proceed to checkout <br>2. Review product list, price, shipping, total | All items and amounts shown correctly                                     | High     |

2. PAYMENT MODULE – Functional Test Cases
| TC ID | Test Case Title                                                  | Steps                                                                          | Expected Result                                             | Priority |
| ----- | ---------------------------------------------------------------- | ------------------------------------------------------------------------------ | ----------------------------------------------------------- | -------- |
| PY_01 | Verify display of available payment methods                      | 1. On payment step, view available options (Credit, Debit, Wallets)            | All configured payment methods listed                       | High     |
| PY_02 | Verify successful payment via credit card                        | 1. Select “Credit Card” <br>2. Enter valid card details <br>3. Confirm payment | Payment processed successfully; order confirmation shown    | High     |
| PY_03 | Verify failed payment with invalid card                          | 1. Enter invalid card number/expiry <br>2. Try to pay                          | Error displayed: “Invalid card details” or “Payment failed” | High     |
| PY_04 | Verify payment via digital wallet                                | 1. Select “Wallet” (e.g., Paytm/Google Pay) <br>2. Complete transaction        | Payment success; redirected to order confirmation           | Medium   |
| PY_05 | Verify payment timeout handling                                  | 1. Wait until session times out during payment                                 | System shows “Session expired” or prompts to retry          | Medium   |
| PY_06 | Verify order confirmation email after successful payment         | 1. Complete a successful order <br>2. Check registered email                   | Order confirmation email received with all order details    | High     |
| PY_07 | Verify payment amount matches order total                        | 1. Proceed to payment <br>2. Compare amount charged vs. order total            | Both values match exactly                                   | High     |
| PY_08 | Verify order status update post-payment                          | 1. Place successful order <br>2. Go to “My Orders” page                        | Order status = “Confirmed” or “Processing”                  | High     |
| PY_09 | Verify failed payment does not create order                      | 1. Try invalid transaction                                                     | No order generated; user stays on payment page              | High     |
| PY_10 | Verify refund flow trigger for failed transaction (if supported) | 1. Simulate payment failure post deduction                                     | Refund status displayed as “Initiated”                      | Low      |

