from flask import Flask
from grocery_app.extensions import db, login_manager, bcrypt
from grocery_app.routes import main
from grocery_app.models import User
from .config import Config
import os


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        """Check if user is logged-in on every page load."""
        if user_id is not None:
            return User.query.get(user_id)
        return None

    app.register_blueprint(main)

    from grocery_app.auth_routes import auth as auth_blueprint

    app.register_blueprint(auth_blueprint)

    with app.app_context():
        db.create_all()

    return app
