import unittest

from falken_teleworking import create_app

app = create_app()

class TestMain(unittest.TestCase):
    
    def setUp(self) -> None:
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_home(self):
        response = self.app.get("/")
        self.assertEqual(200, response.status_code)        
        response = self.app.get("/home")
        self.assertEqual(200, response.status_code)
