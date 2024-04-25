from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase, RequestFactory
from django.utils.datastructures import MultiValueDictKeyError

from rest_framework import status


class SPOTIFYTestCases(TestCase):
    PLAYER_URL = reverse('player', kwargs={'url': 'https:++mock_url'})
    CATEGORIES_URL = reverse('categories')
    SEARCH_URL = reverse('search')

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test',
            password='123'
        )
        self.client.force_login(self.user)
        self.factory = RequestFactory()

    def test_valid_player_get_response(self):
        response = self.client.get(self.PLAYER_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'player.html')

    def test_valid_categories_get_response(self):
        response = self.client.get(self.CATEGORIES_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'categories.html')

    def test_valid_search_post_response(self):
        data = {
            'search_text': 'Linkin park',
            'search_type': 'artist'
        }
        response = self.client.post(self.SEARCH_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'search.html')

    def test_invalid_search_post_response(self):
        data = {
            'search': 'artidasfdafst'
        }
        try:
            response = self.client.post(self.SEARCH_URL, data=data)
            self.assertNotEqual(response.status_code, status.HTTP_200_OK)
        except MultiValueDictKeyError:
            self.assertTrue(True)
