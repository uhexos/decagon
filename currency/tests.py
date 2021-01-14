from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.urls import reverse
import json

# Create your tests here.
# Make all requests in the context of a logged in session.
# client.login(username='admin', password='password')
token = Token.objects.get(user__username='admin')
client = APIClient()
client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

class UserRegistrationTestCase(APITestCase):
    url = reverse("customuser-list")

    def test_invalid_password(self):
        """
        Test to verify that a post call with invalid passwords
        """
        user_data = {
            "username": "testuser",
            "email": "test@testuser.com",
            "password": "siabb2014",
            "re_password": "siabb20141"
        }
        response = self.client.post(self.url, user_data)
        self.assertEqual(400, response.status_code)

    def test_user_registration(self):
        """
        Test to verify that a post call with user valid data
        """
        user_data = {
            "username": "testuser",
            "email": "test@testuser.com",
            "password": "siabb2014",
            "re_password": "siabb2014"
        }
        response = self.client.post(self.url, user_data)
        print(response.content)

        self.assertEqual(201, response.status_code)
        self.assertTrue("id" in json.loads(response.content))

    def test_unique_username_validation(self):
        """
        Test to verify that a post call with already exists username
        """
        user_data_1 = {
            "username": "testuser",
            "email": "test@testuser.com",
            "password": "siabb2014",
            "re_password": "siabb2014"
        }
        response = self.client.post(self.url, user_data_1)
        self.assertEqual(201, response.status_code)

        user_data_2 = {
            "username": "testuser",
            "email": "test2@testuser.com",
            "password": "siabb2014",
            "re_password": "siabb2014"
        }
        response = self.client.post(self.url, user_data_2)
        self.assertEqual(400, response.status_code)
