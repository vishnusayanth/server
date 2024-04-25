from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import *

router = DefaultRouter()
router.register('countries', CountryAPIView, basename='country')
router.register('continents', ContinentAPIView, basename='continent')
app_name = 'api'
urlpatterns = [
    path('', include(router.urls)),
    path('countries_in_continent/<int:continent>', countries_in_continent_api, name='countries_in_continent'),
    path('states/<int:country>', states, name='states'),
    path('capital/<int:country>', capital, name='capital'),
]
