from flask import Blueprint,abort, render_template, request, redirect, url_for,Flask,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Product,ShoppingCart,User,Order,OrderItem,RegistrationForm,LoginForm
from . import db

main = Blueprint('main', __name__)

# LOGIN REGISTER 
# Register route
@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('Email already registered. Please log in.', 'danger')
            return redirect(url_for('main.login'))

        # Hash the password using pbkdf2:sha256 (default method)
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html', form=form)

# Login route
@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):  # Validate hashed password
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html', form=form)



# Logout route
@main.route('/logout')
@login_required
def logout():
    logout_user()  # Log the user out
    flash('You have been logged out.', 'info')  
    return redirect(url_for('main.login')) 


# Protect all routes except the public ones
@main.before_request
def before_request():
    if request.endpoint not in ['main.home', 'main.login', 'main.register', 'main.logout']:
        if not current_user.is_authenticated:
            flash('You need to log in first!', 'warning')
            return redirect(url_for('main.login'))  # Use 'main.login'

# ADMIN ROUTE

@main.route('/admin/products')
@login_required
def manage_products():
    """Route to display all products."""
    products = Product.query.all()
    return render_template('manage_products.html', products=products)

@main.route('/admin/products/add', methods=['GET', 'POST'])
@login_required
def add_product():
    """Route to add a new product."""
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        image = request.form['image']

        new_product = Product(name=name, description=description, price=price, image=image)
        db.session.add(new_product)
        db.session.commit()

        return redirect(url_for('main.manage_products'))

    return render_template('add_product.html')

@main.route('/admin/products/delete/<int:id>')
@login_required
def delete_product(id):
    """Route to delete a product."""
    product = Product.query.get(id)
    if product:
        db.session.delete(product)
        db.session.commit()
    return redirect(url_for('main.manage_products'))


# MAIN ROUTES

@main.route('/')
def home():
    products = Product.query.all()  # Fetch all products from the database
    return render_template('product_listing.html', products=products)


# PRODUCT ROUTES

@main.route('/products')
@login_required
def product_listing():
    """Display all available products."""
    products = Product.query.all()  # Fetch all products from the database
    return render_template('product_listing.html', products=products)


@main.route('/product/<int:product_id>')
@login_required
def product_details(product_id):
    """Display details of a specific product."""
    product = Product.query.get(product_id)
    if not product:
        return render_template('error.html', message="Product not found"), 404  # Display an error page if not found

    return render_template('product_details.html', product=product)

# CART ROUTES
@main.route('/cart')
@login_required
def shopping_cart():
    """View items in the shopping cart."""
    user_id = 1  # Assume a logged-in user (mock for now)
    cart_items = ShoppingCart.query.filter_by(user_id=user_id).all()

    products = {item.product_id: Product.query.get(item.product_id) for item in cart_items}

    for item in cart_items:
        # Query the product based on product_id
        product = Product.query.get(item.product_id)
        if product:
            products[item.product_id] = product
        else:
            print(f"Product with ID {item.product_id} not found.")  # Debugging

    # Calculate total cost for the cart
    total_price = sum(item.quantity * products[item.product_id].price for item in cart_items)
    cart_total =f"{total_price:.2f}"
    return render_template('shopping_cart.html', cart_items=cart_items, products=products, cart_total=cart_total)


@main.route('/cart/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    """Add a product to the shopping cart."""
    user_id = 1  # Assume a logged-in user (mock for now)
    quantity = int(request.form['quantity'])

    # Check if the product exists
    product = Product.query.get(product_id)
    if not product:
        return render_template('error.html', message="Product not found"), 404
    
    # Check if the item is already in the cart
    cart_item = ShoppingCart.query.filter_by(user_id=user_id, product_id=product_id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        new_cart_item = ShoppingCart(user_id=user_id, product_id=product_id, quantity=quantity)
        db.session.add(new_cart_item)

    db.session.commit()
    return redirect(url_for('main.shopping_cart'))


@main.route('/cart/update/<int:cart_id>', methods=['POST'])
@login_required
def update_cart(cart_id):
    """Update the quantity of a product in the cart."""
    cart_item = ShoppingCart.query.get(cart_id)
    if not cart_item:
        return render_template('error.html', message="Cart item not found"), 404

    cart_item.quantity = int(request.form['quantity'])
    db.session.commit()
    return redirect(url_for('main.shopping_cart'))


@main.route('/cart/remove/<int:item_id>', methods=['GET'])
@login_required
def remove_from_cart(item_id):
    """Remove an item from the shopping cart."""
    cart_item = ShoppingCart.query.get(item_id)
    if not cart_item:
        return render_template('error.html', message="Cart item not found"), 404

    db.session.delete(cart_item)
    db.session.commit()
    return redirect(url_for('main.shopping_cart'))

# CHECKOUT ROUTES
@main.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    """Handle the checkout process."""
    user_id = 1  # Mock user ID (replace with actual user authentication logic)
    cart_items = ShoppingCart.query.filter_by(user_id=user_id).all()

    # Fetch product details for items in the cart
    products = {item.product_id: Product.query.get(item.product_id) for item in cart_items if Product.query.get(item.product_id)}

    # Calculate the total cart value
    cart_total = sum(
        item.quantity * products[item.product_id].price
        for item in cart_items if item.product_id in products
    )

    if request.method == 'POST':
        # Create a new order
        order = Order(user_id=user_id, status='Pending')
        db.session.add(order)
        db.session.commit()

        # Add each item in the cart to the order
        for item in cart_items:
            product = products.get(item.product_id)
            if product:
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price=product.price
                )
                db.session.add(order_item)

        # Clear the shopping cart after checkout
        ShoppingCart.query.filter_by(user_id=user_id).delete()
        db.session.commit()

        # Redirect to the order confirmation page
        return render_template('order_confirmation.html', order_id=order.id)

    # Render the checkout page with cart details
    return render_template(
        'checkout.html',
        cart_items=cart_items,
        products=products,
        cart_total=cart_total
    )



@main.route('/checkout/submit', methods=['POST'])
@login_required
def checkout_submit():
    """Handle order submission."""
    user_id = 1  # Mock user ID, replace with actual logged-in user ID
    cart_items = ShoppingCart.query.filter_by(user_id=user_id).all()

    if not cart_items:
        return render_template('error.html', message="Your cart is empty. Please add items before checking out."), 400

    # Calculate the total price
    total_price = sum(item.quantity * Product.query.get(item.product_id).price for item in cart_items)

    # Create a new Order
    new_order = Order(
        user_id=user_id,
        total_price=total_price,
        status="Confirmed"  # Set initial status
    )
    db.session.add(new_order)
    db.session.commit()  # Save the order to get the order ID

    # Add items to the order
    for cart_item in cart_items:
        product = Product.query.get(cart_item.product_id)
        if product:
            order_item = OrderItem(
                order_id=new_order.id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                price=product.price
            )
            db.session.add(order_item)

    # Clear the cart
    ShoppingCart.query.filter_by(user_id=user_id).delete()
    db.session.commit()

    return render_template('thank_you.html', order_id=new_order.id)



# ORDER ROUTES

@main.route('/orders')
@login_required
def order_history():
    """Display the user's order history."""
    user_id = 1  # Mock user ID
    orders = Order.query.filter_by(user_id=user_id).all()
    return render_template('order_history.html', orders=orders)

@main.route('/order/<int:order_id>', methods=['GET'])
@login_required
def order_details(order_id):
    order = Order.query.get(order_id)
    # If order is not found, handle the error
    if order is None:
        return abort(404)
    return render_template('order_details.html', order=order)



