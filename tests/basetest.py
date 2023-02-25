import unittest
import os
from flask import Flask

from falken_teleworking import db
from falken_teleworking.auth import auth as auth_blueprint
from falken_teleworking.main import main as main_blueprint

basedir = os.path.abspath(os.path.dirname(__file__))

class BaseTestCase(unittest.TestCase):

    def setUp(self) -> None:
        """ Creates a new database for the unit test to use """
        self.app = Flask(__name__, template_folder="../templates",
                    static_folder="../static")
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
        db.init_app(self.app)
        # Register blueprints
        self.app.register_blueprint(auth_blueprint)
        self.app.register_blueprint(main_blueprint)

        self.client = self.app.test_client()

        # Crea un contexto de aplicación
        self.app.app_context().push()
        with self.app.app_context():
            # Crea las tablas de la base de datos
            db.create_all()

    def tearDown(self):
        """ Ensures that the database is emptied for next unit test """
        with self.app.app_context():
            # Elimina todas las tablas de la base de datos
            db.session.remove()
            db.drop_all()