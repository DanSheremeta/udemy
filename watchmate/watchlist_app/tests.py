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
        self.assertEqual(WatchList.objects.get(id=1).storyline, 'test storyline - new')

    def test_wl_delete(self):
        response = self.client.delete(reverse('watch-list-details', args=(1,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(WatchList.objects.count(), 0)


class ReviewTestCase(APITestCase):

    def setUp(self):
        self.stream = StreamPlatform.objects.create(name='test sp', about='test about sp',
                                                    website='https://www.test.com/')
        self.watchlist1 = WatchList.objects.create(title='test title 1', storyline='test storyline 1',
                                                   active=True, platform=self.stream,)
        self.watchlist2 = WatchList.objects.create(title='test title 2', storyline='test storyline 2',
                                                   active=True, platform=self.stream,)
        self.user = User.objects.create_user(username='test', password='password')
        self.token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.data = {
            'review_user': self.user,
            'rating': 3,
            'desc': 'test desc',
            'watchlist': self.watchlist1,
            'active': True,
        }
        self.review = Review.objects.create(**self.data)

    def test_review_create(self):
        self.data['rating'] = 5
        self.data['desc'] += ' - new'
        self.data['watchlist'] = self.watchlist2
        response = self.client.post(reverse('review-create', args=(self.watchlist2.id,)), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.get(id=self.watchlist2.id).rating, 5)
        self.assertEqual(Review.objects.get(id=self.watchlist2.id).desc, 'test desc - new')
        self.assertEqual(Review.objects.count(), 2)

        response = self.client.post(reverse('review-create', args=(self.watchlist2.id,)), self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_review_create_unauth(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.post(reverse('review-create', args=(self.watchlist2.id,)), self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_review_change(self):
        self.data['rating'] = 2
        self.data['desc'] += ' - new'
        self.data['active'] = False
        response = self.client.put(reverse('review-detail', args=(self.review.id,)), self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(Review.objects.get(id=self.watchlist1.id).rating, 2)
        self.assertEqual(Review.objects.get(id=self.watchlist1.id).desc, 'test desc - new')
        self.assertEqual(Review.objects.get(id=self.watchlist1.id).active, False)

    def test_review_list(self):
        response = self.client.get(reverse('review-list', args=(self.watchlist1.id,)), self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(Review.objects.count(), 1)

    def test_review_by_id(self):
        response = self.client.get(reverse('review-detail', args=(self.review.id,)), self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['rating'], 3)
        self.assertEqual(response.data['desc'], 'test desc')
        self.assertEqual(response.data['active'], True)

    def test_review_delete(self):
        response = self.client.delete(reverse('review-detail', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Review.objects.count(), 0)

    def test_user_review(self):
        response = self.client.get('/api/movies/user-reviews/?username=' + self.user.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
