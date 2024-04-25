from django.contrib import admin

from locations.models import Continent, Country, State

admin.site.register(Continent)
admin.site.register(Country)
admin.site.register(State)
