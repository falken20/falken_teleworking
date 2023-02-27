import unittest

from . import basetest


class TestMain(basetest.BaseTestCase):

    def test_home(self):
        response = self.client.get("/")
        print(response.text)
        self.assertEqual(200, response.status_code)        
        response = self.client.get("/home")
        self.assertEqual(200, response.status_code)
