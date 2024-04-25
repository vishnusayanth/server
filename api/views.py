from django.db.models import Q
from django.shortcuts import redirect
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.serializers import CountrySerializer, ContinentSerializer
from locations.models import Country, Continent, State
from server.classes import DjangoAppLogger

logger = DjangoAppLogger(__name__)


class CountryAPIView(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = Country.objects.all()
    permission_classes = IsAuthenticated,
    serializer_class = CountrySerializer
    authentication_classes = TokenAuthentication,

    def list(self, request, *args, **kwargs):
        data = {
            'countries': self.get_serializer(self.queryset, many=True).data
        }
        # list function is overridden to create a custom response
        return Response(data=data, status=status.HTTP_200_OK, content_type='application/json')

    def retrieve(self, request, *args, **kwargs):
        # object is retrieved from database using primary key from kwargs.
        obj = Country.objects.get(id=kwargs['pk'])
        response = {
            'id': obj.id,
            'name': obj.name,
            'official_language': obj.official_language,
            'country_code': obj.country_code,
            'iso_code': obj.iso_code,
            'continent': obj.continent.name
        }
        # Dictionary is returned in form of Response with status code 200
        return Response(data=response, status=status.HTTP_200_OK)


class ContinentAPIView(viewsets.GenericViewSet):
    queryset = Continent.objects.all()
    permission_classes = IsAuthenticated,
    serializer_class = ContinentSerializer
    authentication_classes = TokenAuthentication,

    def list(self, request, *args, **kwargs):
        data = {
            'continents': self.get_serializer(self.queryset, many=True).data
        }
        # list function is overridden to create a custom response
        return Response(data=data, status=status.HTTP_200_OK, content_type='application/json')


@api_view(["GET"])
def states(request, country):
    try:
        return Response({
            'country': Country.objects.get(id=country).name,
            'states': list(State.objects.filter(country_id=country).values('name'))
        })
    except Exception as ex:
        logger.write_to_console(str(ex),traceback, 'states')
        return redirect('error')


@api_view(["GET"])
def countries_in_continent_api(request, continent):
    try:
        return Response({
            'continent': Continent.objects.get(id=continent).name,
            'countries': list(Country.objects.filter(continent_id=continent).values('name'))
        })
    except Exception as ex:
        logger.write_to_console(str(ex),traceback, 'countries in continents')
        return redirect('error')


@api_view(["GET"])
def capital(request, country):
    try:
        state = State.objects.get(Q(country_id=country) & Q(capital_state=True))
        return Response({
            'country': Country.objects.get(id=country).name,
            'capital': state.name
        }, content_type='application/json')
    except Exception as ex:
        logger.write_to_console(str(ex),traceback, 'capital')
        return redirect('error')

