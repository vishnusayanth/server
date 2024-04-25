from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from locations.models import Continent, Country, State


class APITestCases(TestCase):
    API_COUNTRIES_URL = reverse('api:country-list')
    API_COUNTRIES_IN_CONTINENT_URL = reverse('api:countries_in_continent', kwargs={'continent': 1})
    API_STATES_URL = reverse('api:states', kwargs={'country': 1})
    API_CONTINENTS_URL = reverse('api:continent-list')
    API_CAPITAL_URL = reverse('api:capital', kwargs={'country': 1})
    API_COUNTRY_URL = reverse('api:country-detail', kwargs={'pk': 1})

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='test',
            password='testpass'
        )
        self.client.force_authenticate(self.user)
        self.factory = RequestFactory()

    def test_valid_continents_get_response(self):
        data = self.client.get(self.API_CONTINENTS_URL)
        self.assertEqual(data.status_code, status.HTTP_200_OK)

    def test_valid_countries_get_response(self):
        data = self.client.get(self.API_COUNTRIES_URL)
        self.assertEqual(data.status_code, status.HTTP_200_OK)

    def test_valid_states_get_response(self):
        self.client.force_login(self.user)
        continent = Continent.objects.create(name="asia")
        country = Country.objects.create(name='India', continent=continent, official_language='Hindi', country_code=91,
                                         iso_code='In/Ind')
        State.objects.create(name='Delhi', country=country, capital_state=True)
        data = self.client.get(self.API_STATES_URL)
        self.assertEqual(data.status_code, status.HTTP_200_OK)

    def test_get_capital_valid_response(self):
        self.client.force_login(self.user)
        continent = Continent.objects.create(name="asia")
        country = Country.objects.create(name='India', continent=continent, official_language='Hindi', country_code=91,
                                         iso_code='In/Ind')
        obj = State.objects.create(name='Delhi', country=country, capital_state=True)
        response = self.client.get(self.API_CAPITAL_URL)
        self.assertEqual(response.json()['capital'], obj.name)
        self.assertEqual(response.json()['country'], country.name)

    def test_valid_get_country_response(self):
        continent = Continent.objects.create(name="asia")
        country = Country.objects.create(name='India', continent=continent, official_language='Hindi', country_code=91,
                                         iso_code='In/Ind')
        response = self.client.get(self.API_COUNTRY_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], country.name)
        self.assertEqual(response.data['official_language'], country.official_language)

    def test_valid_countries_in_continents_get_response(self):
        self.client.force_login(self.user)
        Continent.objects.create(name="asia")
        data = self.client.get(self.API_COUNTRIES_IN_CONTINENT_URL)
        self.assertEqual(data.status_code, status.HTTP_200_OK)

    def test_login_required_get_countries(self):
        self.client.logout()
        res = self.client.get(self.API_COUNTRIES_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_required_get_states(self):
        continent = Continent.objects.create(name="asia")
        Country.objects.create(name='India', continent=continent, official_language='Hindi', country_code=91,
                               iso_code='In/Ind')
        self.client.logout()
        res = self.client.get(self.API_STATES_URL)
        self.assertNotEqual(res.status_code, status.HTTP_200_OK)

    def test_login_required_get_continents(self):
        self.client.logout()
        res = self.client.get(self.API_CONTINENTS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_required_capital(self):
        continent = Continent.objects.create(name="asia")
        country = Country.objects.create(name='India', continent=continent, official_language='Hindi', country_code=91,
                                         iso_code='In/Ind')
        State.objects.create(name='Delhi', country=country, capital_state=True)
        self.client.logout()
        res = self.client.get(self.API_CAPITAL_URL)
        self.assertNotEqual(res.status_code, status.HTTP_200_OK)

    def test_login_required_countries_in_continent(self):
        continent = Continent.objects.create(name="asia")
        Country.objects.create(name='India', continent=continent, official_language='Hindi', country_code=91,
                               iso_code='In/Ind')
        self.client.logout()
        res = self.client.get(self.API_COUNTRIES_IN_CONTINENT_URL)
        self.assertNotEqual(res.status_code, status.HTTP_200_OK)
