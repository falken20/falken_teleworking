import unittest

from . import basetest


class TestMain(basetest.BaseTestCase):

    def test_home(self):
        response = self.app.get("/")
        print(response.text)
        self.assertEqual(200, response.status_code)        
        response = self.app.get("/home")
        self.assertEqual(200, response.status_code)
