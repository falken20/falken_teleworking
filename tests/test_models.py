import unittest
from flask import Flask

from falken_teleworking.models import db, Teleworking

TEST_ROW = {"work_day": "01/01/2023", "work_home": "True"}

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
        self.assertIn("Day:", repr(Teleworking.create_day(TEST_ROW)))

    def test_get_all_days(self):
        Teleworking.create_day(TEST_ROW)
        self.assertEqual(1, len(Teleworking.get_all_days()))

    def test_get_count_days(self):
        Teleworking.create_day(TEST_ROW)
        print(TEST_ROW.get("work_day"))
        self.assertEqual(1, Teleworking.get_count_days(TEST_ROW.get("work_day")))