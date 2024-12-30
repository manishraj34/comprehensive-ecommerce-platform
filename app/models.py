from . import db
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_login import UserMixin
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
class User(db.Model,UserMixin):
    """Model for storing user details."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    orders = db.relationship('Order', backref='user', lazy=True)

    @property
    def is_active(self):
        return True  # Or return a condition based on your app logic (e.g., check if user is not banned)

    def __repr__(self):
        return f"<User {self.username}>"

    # You may also need to implement the get_id() method
    def get_id(self):
        return str(self.id)

# Create a registration form with Flask-WTF
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


# Create a login form with Flask-WTF
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class Product(db.Model):
    """Model for storing product details."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f"<Product {self.name}>"


class Order(db.Model):
    """Model for storing orders."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False, default="Pending")
    items = db.relationship('OrderItem', backref='order', lazy=True)

    def __repr__(self):
        return f"<Order {self.id} - Status: {self.status}>"


class OrderItem(db.Model):
    """Model for storing individual items in an order."""
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<OrderItem ProductID: {self.product_id}, Quantity: {self.quantity}>"


class ShoppingCart(db.Model):
    """Model for storing shopping cart items for a user."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<ShoppingCart UserID: {self.user_id}, ProductID: {self.product_id}, Quantity: {self.quantity}>"
