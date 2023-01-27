# by Richi Rod AKA @richionline / falken20
# ./falken_teleworking/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv, find_dotenv

from .models import db
from .logger import Log, console
from .config import get_settings

console.rule("Falken Teleworking")
# Set environment vars
load_dotenv(find_dotenv())
settings = get_settings()
Log.info(f"Settings: {settings}")


def create_app():
    app = Flask(__name__, template_folder="../templates",
                static_folder="../static")

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['TEMPLATE_AUTO_RELOAD'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL'].replace(
        "://", "ql://", 1)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db.init_app(app)

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
