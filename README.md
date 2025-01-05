# Comprehensive E-commerce Platform

## 1. Overview
The Comprehensive E-commerce Platform is a robust web application designed to provide users with a seamless shopping experience. It includes functionalities for browsing products, adding items to the cart, managing orders, and analyzing sales. This platform is built using Python and Flask, with SQLAlchemy for database management. It focuses on scalability, user-friendliness, and responsive design.

---

## 2. Objectives
- **User-Friendly Interface**: Provide an intuitive UI for users to browse products, manage their shopping cart, and complete transactions.
- **Admin Capabilities**: Enable administrators to manage products, analyze sales, and view order history.
- **Scalable Backend**: Leverage Flask and SQLAlchemy for a scalable and efficient backend.
- **Responsive Design**: Ensure compatibility across devices using Bootstrap for responsive layouts.
- **Secure Transactions**: Implement secure API integrations and user authentication mechanisms.

---

## 3. Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Virtual Environment (optional but recommended)
- Flask and its dependencies
- SQLAlchemy for database handling

### Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/comprehensive-ecommerce-platform.git
   cd comprehensive-ecommerce-platform
   ```

2. **Set Up Virtual Environment** (optional):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # For Linux/Mac
   .venv\Scripts\activate    # For Windows
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the Database**:
   - Initialize the database:
     ```bash
     flask db init
     flask db migrate
     flask db upgrade
     ```

5. **Run the Application**:
   ```bash
   python app.py
   ```
   Open your browser and navigate to `http://127.0.0.1:5000`.

---

## 4. Usage Instructions

### For Users
1. **Browse Products**: Explore the available products on the home page.
2. **Add to Cart**: Select products and add them to your shopping cart.
3. **View Cart**: Check the cart summary and proceed to checkout.
4. **Order History**: View the history of your orders (requires login).

### For Administrators
1. **Add Products**: Use the "Add Product" feature to add new products to the catalog.
2. **Manage Products**: Edit or delete existing products.
3. **View Analytics**: Analyze sales data using visualized dashboards.
4. **View Sales**: Check the sales history for all transactions.

## Routes and Their Uses
### Public Routes
1. `/` - Home page displaying product listings.
2. `/login` - User login page.
3. `/register` - User registration page.

### User-Specific Routes
1. `/cart` - Displays the shopping cart with options to manage items.
2. `/cart/add/<product_id>` - Adds a product to the user's cart.
3. `/cart/remove/<item_id>` - Removes an item from the cart.
4. `/orders` - Displays the order history for the logged-in user.
5. `/checkout` - Initiates the checkout process for the user's cart.
6. `/logout` - Logs the user out of the platform.

### Admin-Specific Routes
1. `/admin/add_product` - Page for adding new products.
2. `/admin/manage_products` - Page to view, edit, or delete products.
3. `/admin/analytics` - Displays sales analytics and performance metrics.
4. `/admin/sales` - View detailed sales data.
---

## 5. Known Issues
1. **Cart Persistence**: The cart does not persist after logout; this will be addressed in future updates.
2. **Product Deletion**: Deleting a product may result in orphaned cart items; validation is required.
3. **Error Handling**: Some edge cases (e.g., invalid user input) need better error handling.

---

Feel free to contribute or report issues on the [GitHub repository](https://github.com/manishraj34/comprehensive-ecommerce-platform/tree/main).
