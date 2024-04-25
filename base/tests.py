from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.urls import reverse
from rest_framework import status


class BASETestCases(TestCase):
    HOME_URL = reverse('home')
    CONTACT_URL = reverse('contact')
    DOCS_URL = reverse('docs')
    RESET_PASSWORD_URL = reverse('resetpassword')
    LOGIN_URL = reverse('login')
    ERROR_URL = reverse('error')

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test',
            password='123'
        )
        self.client.force_login(self.user)
        self.factory = RequestFactory()

    def test_valid_home_get_response(self):
        response = self.client.get(self.HOME_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'home.html')

    def test_valid_docs_get_response(self):
        response = self.client.get(self.DOCS_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'docs.html')

    def test_valid_error_get_response(self):
        response = self.client.get(self.ERROR_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'error.html')

    def test_valid_contact_post_response(self):
        data = {
            'name': 'Linkin park',
            'subject': 'artist',
            'email': 'artist',
            'location': 'artist',
            'message': 'artist',
        }
        response = self.client.post(self.CONTACT_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_valid_reset_password_get_response(self):
        response = self.client.get(self.RESET_PASSWORD_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'resetpassword.html')

    def test_valid_login_get_response(self):
        response = self.client.get(self.LOGIN_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'login.html')
