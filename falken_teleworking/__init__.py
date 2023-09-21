# by Richi Rod AKA @richionline / falken20
# ./falken_teleworking/__init__.py

from flask import Flask
import os
from dotenv import load_dotenv, find_dotenv
from flask_login import LoginManager

from .models import db
from .logger import Log, console
from .config import get_settings
from .main import check_cache

console.rule("Falken Teleworking")
# Set environment vars
load_dotenv(find_dotenv())
settings = get_settings()
Log.info(f"Settings: \n env_name: {settings.env_name}\
         \n ENV_PRO: {settings.ENV_PRO}\
         \n LEVEL_LOG: {settings.LEVEL_LOG}")

# Cache info
check_cache()


def create_app():
    app = Flask(__name__, template_folder="../templates",
                static_folder="../static")

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-special-secret-key')
    app.config['TEMPLATE_AUTO_RELOAD'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL'].replace(
        "://", "ql://", 1)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db.init_app(app)

    # A user loader tells Flask-Login how to find a specific user from the ID that is stored in their
    # session cookie.
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # Since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
