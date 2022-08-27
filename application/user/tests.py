"""
Tests for user api
"""


from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status


def create_user(**params):
    """Create and return a new user."""

    return get_user_model().objects.create_user(**params)


class CreateUserApiTest(TestCase):
    """Test create user api"""
    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating user successful"""

        payload = {
            'username': 'testuser1',
            'password': 'testpass001',
            'email': 'test001@example.com',
            'first_name': 'test_f_name001',
            'last_name': 'test_l_name001',
        }

        res = self.client.post('/api/createuser/', payload)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_user_with_email_exists_error(self):
        """"Test error returned if with email exists."""
        payload = {
            'username': 'testuser1',
            'password': 'testpass001',
            'email': 'test001@example.com',
            'first_name': 'test_f_name001',
            'last_name': 'test_l_name001',
        }

        create_user(**payload)
        res = self.client.post('/api/createuser/', payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_missing_password_field_error(self):
        """Test an error returned if password is missing from post data"""
        payload = {
            'username': 'testuser1',
            'email': 'test001@example.com',
            'first_name': 'test_f_name001',
            'last_name': 'test_l_name001',
        }

        res = self.client.post('/api/createuser/', payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_missing_username_field_error(self):
        """Test an error returned if password is missing from post data"""
        payload = {
            'password': 'testpass123',
            'email': 'test001@example.com',
            'first_name': 'test_f_name001',
            'last_name': 'test_l_name001',
        }

        res = self.client.post('/api/createuser/', payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_for_user(self):
        """Test generates token for valid credentials."""

        user_details = {
            'username': 'testuser1',
            'password': 'testpass001',
            'email': 'test001@example.com',
            'first_name': 'test_f_name001',
            'last_name': 'test_l_name001',
        }

        create_user(**user_details)

        payload = {
            'username': user_details['username'],
            'password': user_details['password'],
        }

        res = self.client.post('/api/token/', payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Test generates token for valid credentials."""

        user_details = {
            'username': 'testuser1',
            'password': 'testpass001',
            'email': 'test001@example.com',
            'first_name': 'test_f_name001',
            'last_name': 'test_l_name001',
        }

        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': 'wrongpass',
        }

        res = self.client.post('/api/token/', payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
