import unittest
import os

from . import basetest


class TestAuth(basetest.BaseTestCase):
    
    def login_http(self):
        # log in via HTTP
        r = self.app.post('/login', 
                          data={'username': 'python', 'password': 'password'})
        assert r.status_code == 200

    def test_login(self):
        response = self.app.get("/login")
        self.assertEqual(200, response.status_code)        

    def test_signup(self):
        response = self.app.get("/signup")
        self.assertEqual(200, response.status_code)

    def test_logout(self):
        self.login_http()
        response = self.app.get("/logout")
        print(response.text)
        self.assertEqual(200, response.status_code)