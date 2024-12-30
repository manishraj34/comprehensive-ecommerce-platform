from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    """Create and configure the Flask app."""
    app = Flask(__name__)

    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'  # Use SQLite for simplicity
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your_secret_key'

    db.init_app(app)

    # Initialize LoginManager
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    # Register Blueprints
    from .routes import main
    app.register_blueprint(main)


    # Initialize database tables
    with app.app_context():
        db.create_all()

    return app


@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(int(user_id))