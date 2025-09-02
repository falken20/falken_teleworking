import unittest
from flask import Flask
from datetime import date
from unittest.mock import patch
from io import StringIO

from falken_teleworking.models import Teleworking, init_db, User
from . import basetest

TEST_DATE = date.today()
TEST_ROW = {"date": TEST_DATE, "work_home": "True", "work_user": 1}


class TestModels(basetest.BaseTestCase):

    def test_repr(self):
        self.assertIn("Day:", repr(Teleworking.create_day(TEST_ROW, user_id=TEST_ROW['work_user'])))

    def test_get_all_data(self):
        Teleworking.create_day(TEST_ROW, user_id=TEST_ROW['work_user'])
        self.assertEqual(1, len(Teleworking.get_all_data(user_id=TEST_ROW['work_user'])))

    def test_get_all_dates(self):
        Teleworking.create_day(TEST_ROW, user_id=TEST_ROW['work_user'])
        self.assertEqual(1, len(Teleworking.get_all_dates(user_id=TEST_ROW['work_user'])))

    def test_get_count_days(self):
        Teleworking.create_day(TEST_ROW, user_id=TEST_ROW['work_user'])
        self.assertEqual(1, Teleworking.get_count_days(True, user_id=TEST_ROW['work_user']))

    def test_get_day(self):
        Teleworking.create_day(TEST_ROW, user_id=TEST_ROW['work_user'])
        self.assertEqual(1, Teleworking.get_day(TEST_ROW['date'], TEST_ROW['work_user']).work_user)

    @patch('sys.stdin', StringIO('N\nN\n'))  # Simulate user input
    def test_init_db(self):
        init_db(self.app)

    @patch('sys.stdin', StringIO('y\ny\n'))  # Simulate user input
    def test_init_db_with_drop(self):
        init_db(self.app)
    
    @patch('sys.stdin', StringIO('N\nY\n'))  # Simulate user input
    def test_init_db_with_create(self):
        init_db(self.app)

    def test_get_user_date(self):
        date_from = User.get_user_date(user_id=TEST_ROW['work_user']).date_from
        self.assertTrue(isinstance(date_from, date))
