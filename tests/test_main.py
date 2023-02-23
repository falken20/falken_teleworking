import unittest

from falken_teleworking import create_app, db


class TestMain(unittest.TestCase):
  
    def setUp(self) -> None:
        app = create_app()
        app.config['TESTING'] = True
        self.app = app.test_client()
        # Dynamically bind SQLAlchemy to application
        db.init_app(app)
        app.app_context().push()  # this does the binding

    def tearDown(self):
        """
        Ensures that the database is emptied for next unit test
        """
        app = create_app()
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_home(self):
        response = self.app.get("/")
        print(response.text)
        self.assertEqual(200, response.status_code)        
        response = self.app.get("/home")
        self.assertEqual(200, response.status_code)
