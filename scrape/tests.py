from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase, RequestFactory

from rest_framework import status


class SCRAPETestCases(TestCase):
    NEWS_URL = reverse('news')
    FETCH_NEWS_URL = reverse('fetch_news')
    ZOMATO_URL = reverse('zomato')

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test',
            password='123'
        )
        self.client.force_login(self.user)
        self.factory = RequestFactory()

    def test_valid_news_get_response(self):
        response = self.client.get(self.NEWS_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'news.html')

    def test_valid_zomato_get_response(self):
        response = self.client.get(self.ZOMATO_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'zomato.html')

    def test_valid_fetch_news_get_response(self):
        response = self.client.get(self.FETCH_NEWS_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
