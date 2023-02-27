import unittest
import os

from . import basetest


class TestAuth(basetest.BaseTestCase):
    
    def login_http(self):
        basetest.BaseTestCase.create_user(basetest.user)
        # log in via HTTP
        response = self.client.post('/login', basetest.user)
        print(response.text)
        assert response.status_code == 200

    def test_login(self):
        response = self.client.get("/login")
        self.assertEqual(200, response.status_code)        

    def test_signup(self):
        response = self.client.get("/signup")
        self.assertEqual(200, response.status_code)

    def test_logout(self):
        self.login_http()
        response = self.client.get("/logout")
        self.assertEqual(200, response.status_code)