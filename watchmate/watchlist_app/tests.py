from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from .models import WatchList, StreamPlatform, Review


class StreamPlatformTestCase(APITestCase):

    def setUp(self):
        self.data = {
            'name': 'test sp',
            'about': 'test about sp',
            'website': 'https://www.test.com/',
        }
        self.user = User.objects.create_superuser(username='test_superuser',
                                                  password='test_password')
        self.token = Token.objects.get(user__username='test_superuser')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream = StreamPlatform.objects.create(**self.data)

    def test_sp_create(self):
        data = {
            'name': 'test sp second',
            'about': 'test about sp second',
            'website': 'https://www.test-second.com/',
        }
        response = self.client.post(reverse('streamplatform-list'), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(StreamPlatform.objects.count(), 2)

    def test_sp_list(self):
        response = self.client.get(reverse('streamplatform-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_sp_by_id(self):
        response = self.client.get(reverse('streamplatform-detail', args=(1,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'test sp')

    def test_sp_change(self):
        self.data['name'] += ' - new'
        self.data['about'] += ' - new'
        response = self.client.put(reverse('streamplatform-detail', args=(1,)), self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(StreamPlatform.objects.get(id=1).name, 'test sp - new')
        self.assertEqual(StreamPlatform.objects.get(id=1).about, 'test about sp - new')
        self.assertEqual(StreamPlatform.objects.count(), 1)

    def test_sp_delete(self):
        response = self.client.delete(reverse('streamplatform-detail', args=(1,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(StreamPlatform.objects.count(), 0)


class WatchListTestCase(APITestCase):

    def setUp(self):
        self.stream = StreamPlatform.objects.create(name='test sp', about='test about sp',
                                                    website='https://www.test.com/')
        self.data = {
            'title': 'test title',
            'storyline': 'test storyline',
            'active': True,
            'platform': self.stream,
        }
        self.movie = WatchList.objects.create(**self.data)

        self.superuser = User.objects.create_superuser(username='test_superuser', password='test_password')
        self.token = Token.objects.get(user__username='test_superuser')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_wl_list(self):
        response = self.client.get(reverse('watch-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_wl_by_id(self):
        response = self.client.get(reverse('watch-list-details', args=(1,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'test title')
        self.assertEqual(response.data['platform'], 'test sp')

    def test_wl_create(self):
        self.data['title'] += ' - new'
        self.data['storyline'] += ' - new'
        response = self.client.post(reverse('watch-list'), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_wl_change(self):
        self.data['title'] += ' - new'
        self.data['storyline'] += ' - new'
        response = self.client.put(reverse('watch-list-details', args=(1,)), self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(WatchList.objects.get(id=1).title, 'test title - new')

    def test_wl_delete(self):
        response = self.client.delete(reverse('watch-list-details', args=(1,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(WatchList.objects.count(), 0)
