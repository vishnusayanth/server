from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase, RequestFactory

from rest_framework import status

from locations.models import Continent, Country, State


class LOCATIONSTestCases(TestCase):
    COUNTRIES_URL = reverse('countries')
    STATES_URL = reverse('states', kwargs={'country': 1})

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test',
            password='123'
        )
        self.client.force_login(self.user)
        self.factory = RequestFactory()

    def test_valid_countries_get_response(self):
        Continent.objects.create(name='Asia')
        response = self.client.get(self.COUNTRIES_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'countries.html')

    def test_valid_states_get_response(self):
        obj = Continent.objects.create(name='Asia')
        obj.save()
        Country.objects.create(name='India', continent=obj)
        response = self.client.get(self.STATES_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'states.html')

    def test_Continent_model(self):
        obj = Continent.objects.create(name="asia")
        self.assertEqual(str(obj), obj.name)

    def test_Country_model(self):
        continent = Continent.objects.create(name="asia")
        obj = Country.objects.create(name='India', continent=continent, official_language='Hindi', country_code=91,
                                     iso_code='In/Ind')
        self.assertEqual(str(obj), obj.name)

    def test_State_model(self):
        continent = Continent.objects.create(name="asia")
        country = Country.objects.create(name='India', continent=continent, official_language='Hindi', country_code=91,
                                         iso_code='In/Ind')
        obj = State.objects.create(name='Delhi', country=country, capital_state=True)
        self.assertEqual(str(obj), obj.name)
        self.assertEqual(country, obj.country)
