import unittest
import os
from flask import Flask
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
from datetime import date

from falken_teleworking import db
from falken_teleworking.models import User
from falken_teleworking.auth import auth as auth_blueprint
from falken_teleworking.main import main as main_blueprint

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseTestCase(unittest.TestCase):
    mock_user = {'email': 'python@mail.com', 'name': 'python', 'password': 'password'}
    mock_user_unknown = {'email': 'python@mail.com', 'name': 'python', 'password': 'error_password'}    

    def setUp(self) -> None:
        """ Creates a new database for the unit test to use """
        self.app = Flask(__name__, template_folder="../templates",
                    static_folder="../static")
        self.app.config['SECRET_KEY'] = 'secret-key-test'
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
        db.init_app(self.app)
        # Register blueprints
        self.app.register_blueprint(auth_blueprint)
        self.app.register_blueprint(main_blueprint)

        self.config_login()
        self.client = self.app.test_client()

        # Crea un contexto de aplicación
        self.app.app_context().push()
        with self.app.app_context():
            # Crea las tablas de la base de datos
            db.create_all()

        # Create a user
        self.create_user(self.mock_user)

        
    def tearDown(self):
        """ Ensures that the database is emptied for next unit test """
        with self.app.app_context():
            # Elimina todas las tablas de la base de datos
            db.session.remove()
            db.drop_all()

    def config_login(self):
        # A user loader tells Flask-Login how to find a specific user from the ID that is stored in their
        # session cookie.
        login_manager = LoginManager()
        login_manager.login_view = 'auth.login'
        login_manager.init_app(self.app)

        @login_manager.user_loader
        def load_user(user_id):
            # Since the user_id is just the primary key of our user table, use it in the query for the user
            return User.query.get(int(user_id))
        
    @staticmethod
    def create_user(mock_user):
        new_user = User(email=mock_user['email'], name=mock_user['name'],
                    password=generate_password_hash(mock_user['password'], method='sha256'),
                    date_from=date.today())
        db.session.add(new_user)
        db.session.commit()
        return new_user
    
    @staticmethod
    def login_http(self):
        return self.client.post('/login', data=dict(
            email=self.mock_user['email'],
            password=self.mock_user['password']
        ), follow_redirects=True)
