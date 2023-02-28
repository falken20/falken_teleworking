import unittest

from .basetest import BaseTestCase


class TestMain(BaseTestCase):

    def test_home_redirect_login(self):
        response = self.client.get("/")
        self.assertEqual(302, response.status_code)
        self.assertIn('login', response.location)

    def test_home(self):
        BaseTestCase.login_http(self)
        response = self.client.get("/")
        self.assertEqual(200, response.status_code)        
        response = self.client.get("/home")
        self.assertEqual(200, response.status_code)
