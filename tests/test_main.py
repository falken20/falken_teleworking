import unittest
from datetime import date, datetime

from .basetest import BaseTestCase
from falken_teleworking.models import Teleworking


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

    def test_save_a_day_home(self):
        BaseTestCase.login_http(self)
        response = self.client.post("/", data=dict(
            work_home=True
        ))
        self.assertEqual(200, response.status_code)

    def test_save_a_day_office(self):
        BaseTestCase.login_http(self)
        response = self.client.post("/", data=dict(
            work_home=False
        ))
        self.assertEqual(200, response.status_code)

    def test_calendar(self):
        BaseTestCase.login_http(self)
        response = self.client.get("/calendar")
        self.assertEqual(200, response.status_code)

    def test_count_days_home(self):
        BaseTestCase.login_http(self)
        response = self.client.post("/", data=dict(
            work_home=True
        ))
        count_days = Teleworking.get_count_days(True, 1)
        self.assertEqual(1, count_days)

    def test_count_days_office(self):
        BaseTestCase.login_http(self)
        response = self.client.post("/", data=dict(
            work_home=False
        ))
        count_days = Teleworking.get_count_days(False, 1)
        self.assertEqual(1, count_days)

    def test_profile_post(self):
        BaseTestCase.login_http(self)
        date_from = date.today()
        response = self.client.post('/profile', data=dict(date_from=date_from))
        self.assertEqual(302, response.status_code)  # Should redirect after POST

    def test_search(self):
        BaseTestCase.login_http(self)
        response = self.client.get("/search")
        self.assertEqual(200, response.status_code)

    def test_search_post(self):
        BaseTestCase.login_http(self)
        response = self.client.post("/search", data=dict(
            date_to=date.today(),
            date_from=date.today()
        ))
        self.assertEqual(200, response.status_code)
