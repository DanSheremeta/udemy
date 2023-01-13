from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token


class RegisterTestCase(APITestCase):

    def setUp(self):
        self.data = {
            'username': 'testname',
            'email': 'testemail@gmail.com',
            'password': 'testpassword',
            'password2': 'testpassword',
        }

    def test_register(self):
        response = self.client.post(reverse('sign-in'), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_incorrect_password(self):
        self.data['password2'] = 'wrong'
        response = self.client.post(reverse('sign-in'), self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginLogoutTestCase(APITestCase):

    def setUp(self):
        self.data = {
            'username': 'test',
            'password': 'test0password'
        }
        self.user = User.objects.create_user(username='test',
                                             password='test0password')

    def test_login(self):
        response = self.client.post(reverse('login'), self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_incorrect_login(self):
        self.data['password'] = 'wrong'
        response = self.client.post(reverse('login'), self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout(self):
        self.token = Token.objects.get(user__username=self.data['username'])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
