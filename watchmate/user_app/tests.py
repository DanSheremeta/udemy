from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token


class RegisterTestCase(APITestCase):

    def test_register(self):
        data = {
            'username': 'testname',
            'email': 'testemail@gmail.com',
            'password': 'testpassword',
            'password2': 'testpassword',
        }
        response = self.client.post(reverse('sign-in'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_incorrect_password(self):
        data = {
            'username': 'testname',
            'email': 'testemail@gmail.com',
            'password': 'testpassword',
            'password2': 'testpassword2',
        }
        response = self.client.post(reverse('sign-in'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
