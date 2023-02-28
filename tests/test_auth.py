import unittest
import os

from .basetest import BaseTestCase


class TestAuth(BaseTestCase):

    def test_login(self):
        response = self.client.get("/login")
        self.assertEqual(200, response.status_code)        

    def test_login_post(self):
        response = self.client.post('/login', data=dict(
            email=BaseTestCase.mock_user['email'],
            password=BaseTestCase.mock_user['password']
        ), follow_redirects=True)
        self.assertEqual(200, response.status_code)

    def test_login_error(self):
        response = self.client.post('/login', data=dict(
            email=BaseTestCase.mock_user_unknown['email'],
            password=BaseTestCase.mock_user_unknown['password']
        ), follow_redirects=True)
        self.assertIn('Please check your login details and try again.', response.text)
        self.assertEqual(200, response.status_code)
        
    def test_signup(self):
        response = self.client.get("/signup")
        self.assertEqual(200, response.status_code)

    def test_logout_redirect_login(self):
        response = self.client.get("/logout")
        self.assertEqual(302, response.status_code)
        self.assertIn('login', response.location)

    def test_logout(self):
        response = BaseTestCase.login_http(self)
        response = self.client.get("/logout")
        self.assertEqual(302, response.status_code)

    def test_signup_post_user_exists(self):
        response = self.client.post('/signup', data=dict(
            email=BaseTestCase.mock_user['email'],
            name=BaseTestCase.mock_user['name'],
            password=BaseTestCase.mock_user['password'],
        ), follow_redirects=True)
        self.assertIn('Email address already exists.', response.text)
        self.assertEqual(200, response.status_code)

    def test_signup_post_new_user(self):
        response = self.client.post('/signup', data=dict(
            email='email',
            name='name',
            password='mipassword',
        ), follow_redirects=True)
        self.assertEqual(200, response.status_code)