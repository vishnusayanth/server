from rest_framework import serializers

from locations.models import Country, Continent, State


class CountrySerializer(serializers.ModelSerializer):
    continent_name = serializers.CharField(source='continent.name')

    class Meta:
        model = Country
        fields = ('id', 'name', 'official_language', 'country_code', 'iso_code', 'continent_name','capital')
        read_only_fields = ('id',)


class ContinentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Continent
        fields = ('id', 'name')
        read_only_fields = ('id',)


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ('id', 'name')
        read_only_fields = ('id',)
