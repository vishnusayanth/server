from django.urls import path
from django.views.generic import TemplateView

from locations.views import *

urlpatterns = [
    path('', TemplateView.as_view(template_name='dashboard.html', extra_context={'title': 'Dashboard'}),
         name='dashboard'),
    path('import/', import_data_to_database, name='import'),
    path('countries/', CountryView.as_view(), name='countries'),
    path('states/<int:country>', StateView.as_view(), name='states'),
    path('countries_in_continent/<str:continent>', countries_in_continent, name='countries_in_continent'),
]
