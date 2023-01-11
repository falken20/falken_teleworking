import unittest

from falken_teleworking import main

class TestMain(unittest.TestCase):
    
    def setUp(self) -> None:
        main.app.config['TESTING'] = True
        self.app = main.app.test_client()

    def test_home(self):
        response = self.app.get("/")
        self.assertEqual(200, response.status_code)        
        response = self.app.get("/home")
        self.assertEqual(200, response.status_code)