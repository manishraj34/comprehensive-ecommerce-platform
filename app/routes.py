from flask import Blueprint, render_template, request, redirect, url_for
from .models import Product,ShoppingCart,User,Order,OrderItem
from . import db

main = Blueprint('main', __name__)

# ADMIN ROUTE
@main.route('/admin/products')
def manage_products():
    """Route to display all products."""
    products = Product.query.all()
    return render_template('manage_products.html', products=products)

@main.route('/admin/products/add', methods=['GET', 'POST'])
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
def delete_product(id):
    """Route to delete a product."""
    product = Product.query.get(id)
    if product:
        db.session.delete(product)
        db.session.commit()
    return redirect(url_for('main.manage_products'))


# Placeholder data for demonstration
products = [
    {'id': 1, 'name': 'Product 1', 'description': 'Description of Product 1', 'price': 100, 'image': 'https://via.placeholder.com/150'},
    {'id': 2, 'name': 'Product 2', 'description': 'Description of Product 2', 'price': 200, 'image': 'https://via.placeholder.com/150'},
    {'id': 3, 'name': 'Product 3', 'description': 'Description of Product 3', 'price': 300, 'image': 'https://via.placeholder.com/150'},
]

cart = []


@main.route('/')
def home():
    products = Product.query.all()  # Fetch all products from the database
    return render_template('product_listing.html', products=products)


@main.route('/products')
def product_listing():
    """Display all available products."""
    products = Product.query.all()  # Fetch all products from the database
    return render_template('product_listing.html', products=products)


@main.route('/product/<int:product_id>')
def product_details(product_id):
    """Display details of a specific product."""
    product = Product.query.get(product_id)
    if not product:
        return render_template('error.html', message="Product not found"), 404  # Display an error page if not found

    return render_template('product_details.html', product=product)

    
@main.route('/cart')
def shopping_cart():
    """View items in the shopping cart."""
    user_id = 1  # Assume a logged-in user (mock for now)
    cart_items = ShoppingCart.query.filter_by(user_id=user_id).all()

    products = {}
    for item in cart_items:
        # Query the product based on product_id
        product = Product.query.get(item.product_id)
        if product:
            products[item.product_id] = product
        else:
            print(f"Product with ID {item.product_id} not found.")  # Debugging

    # Calculate total cost for the cart
    cart_total = sum([item.quantity * products.get(item.product_id).price if products.get(item.product_id) else 0 for item in cart_items])

    return render_template('shopping_cart.html', cart_items=cart_items, products=products, cart_total=cart_total)


@main.route('/cart/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    """Add a product to the shopping cart."""
    user_id = 1  # Assume a logged-in user (mock for now)
    quantity = int(request.form['quantity'])

    # Check if the item is already in the cart
    cart_item = ShoppingCart.query.filter_by(user_id=user_id, product_id=product_id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        new_cart_item = ShoppingCart(user_id=user_id, product_id=product_id, quantity=quantity)
        db.session.add(new_cart_item)

    db.session.commit()
    return redirect(url_for('main.shopping_cart'))




@main.route('/cart/remove/<int:item_id>', methods=['GET'])
def remove_from_cart(item_id):
    """Remove an item from the shopping cart."""
    cart_item = ShoppingCart.query.get(item_id)
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
    return redirect(url_for('main.shopping_cart'))


@main.route('/checkout', methods=['GET', 'POST'])
def checkout():
    """Route for the Checkout page."""
    if request.method == 'POST':
        # Handle the order submission logic here (mocked for now)
        global cart
        cart = []  # Clear the cart after checkout
        return redirect(url_for('main.home'))
    cart_total = sum(item['quantity'] * item['price'] for item in cart)
    return render_template('checkout.html', cart_items=cart, cart_total=cart_total)

@main.route('/checkout/submit', methods=['POST'])
def checkout_submit():
    """Route to handle order submission."""
    global cart
    cart = []  # Clear the cart after checkout
    return render_template('thank_you.html')
