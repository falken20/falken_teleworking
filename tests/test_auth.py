import unittest

from falken_teleworking import create_app


class TestAuth(unittest.TestCase):
    
    def setUp(self) -> None:
        app = create_app()
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_login(self):
        response = self.app.get("/login")
        self.assertEqual(200, response.status_code)        

    def test_signup(self):
        response = self.app.get("/signup")
        self.assertEqual(200, response.status_code)

    def test_logout(self):
        response = self.app.get("/logout")
        print(response.text)
        self.assertEqual(200, response.status_code)