import unittest
from flask import Flask
from datetime import datetime
from unittest.mock import patch
from io import StringIO

from falken_teleworking.models import db, Teleworking, init_db

TEST_DATE = datetime.now().date()
TEST_ROW = {"work_day": TEST_DATE, "work_home": "True", "work_user": 1}


class TestModels(unittest.TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

        # Dynamically bind SQLAlchemy to application
        db.init_app(app)
        app.app_context().push()  # this does the binding
        return app

    def setUp(self):
        """
        Creates a new database for the unit test to use
        """
        app = self.create_app()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        """
        Ensures that the database is emptied for next unit test
        """
        app = self.create_app()
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_repr(self):
        self.assertIn("Day:", repr(Teleworking.create_day(TEST_ROW, user_id=TEST_ROW['work_user'])))

    def test_get_all_data(self):
        Teleworking.create_day(TEST_ROW, user_id=TEST_ROW['work_user'])
        self.assertEqual(1, len(Teleworking.get_all_data(user_id=TEST_ROW['work_user'])))

    def test_get_all_dates(self):
        Teleworking.create_day(TEST_ROW, user_id=TEST_ROW['work_user'])
        self.assertEqual(1, len(Teleworking.get_all_dates(user_id=TEST_ROW['work_user'])))

    def test_get_count_days(self):
        Teleworking.create_day(TEST_ROW, user_id=TEST_ROW['work_user'])
        self.assertEqual(1, Teleworking.get_count_days(True, user_id=TEST_ROW['work_user']))

    def test_get_day(self):
        Teleworking.create_day(TEST_ROW, user_id=TEST_ROW['work_user'])
        self.assertEqual(1, Teleworking.get_day(TEST_ROW['work_day'], TEST_ROW['work_user']).work_user)

    @patch('sys.stdin', StringIO('N\nN\n'))  # Simulate user input
    def test_init_db(self):
        app = Flask(__name__)
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
        init_db(app)

    @patch('sys.stdin', StringIO('y\ny\n'))  # Simulate user input
    def test_init_db_with_drop(self):
        app = Flask(__name__)
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
        init_db(app)
    
    @patch('sys.stdin', StringIO('N\nY\n'))  # Simulate user input
    def test_init_db_with_create(self):
        app = Flask(__name__)
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
        init_db(app)

