import os
import traceback

import pandas
from django.contrib.auth.decorators import user_passes_test
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic.list import ListView

from locations.models import Country, State, Continent
from server.classes import DjangoAppLogger
from server.settings import MEDIA_ROOT

logger = DjangoAppLogger(__name__)


class CountryView(ListView):
    queryset = Country.objects.all().order_by('name')
    template_name = 'countries.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = self.queryset
        context['title'] = 'Countries'
        return context


class StateView(ListView):
    queryset = State.objects.all().order_by('name')
    template_name = 'states.html'

    def get_queryset(self):
        self.queryset = self.queryset.filter(country__id=self.kwargs['country'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.queryset.first() is not None:
            context['country'] = self.queryset.first().country.name
        context['object_list'] = self.queryset
        context['title'] = 'States'
        return context


def countries_in_continent(request, continent):
    try:
        items = []
        queryset = Country.objects.filter(continent__name=continent).order_by('name')
        if queryset.first() is not None:
            continent = queryset.first().continent.name
        for item in queryset:
            item.capital = State.objects.filter(Q(country_id=item.id) & Q(capital_state=True)).first()
            items.append(item)
        return render(request, 'countries.html',
                      {'object_list': items, 'continent': continent, 'title': 'Countries'})
    except Exception as ex:
        logger.write_to_console(str(ex),traceback, 'countries in continents')
        request.session['message'] = str(ex)
        return redirect('error')


@user_passes_test(lambda u: u.is_superuser)
def import_data_to_database(request):
    """save the file to disk, read it using pandas and delete it after use."""
    message = None
    full_filename = None
    fail = []
    try:
        if request.method == 'POST':
            excel_file = request.FILES["excel_file"]
            full_filename = os.path.join(MEDIA_ROOT, excel_file.name)
            path = default_storage.save(full_filename, ContentFile(excel_file.read()))
            data_frame = pandas.DataFrame(pandas.read_excel(path, engine='openpyxl'))
            if 'states' in request.POST:
                for column in data_frame:
                    try:
                        stripped_column = column.strip()
                        if Country.objects.filter(name=stripped_column).exists():
                            country_id = (Country.objects.get(name=stripped_column)).id
                            for cell in data_frame[column]:
                                if cell != '' and cell is not None:
                                    cell = str(cell).strip().title()
                                    if not State.objects.filter(Q(name=cell) & Q(country_id=country_id)).exists():
                                        obj = State(name=cell, country_id=country_id)
                                        obj.save()
                        else:
                            fail.append(stripped_column)
                    except Exception as ex:
                        logger.write_to_console(str(ex),traceback, 'Import')
            elif 'captials' in request.POST:
                for cell in data_frame['states']:
                    try:
                        if cell != '' and cell is not None:
                            cell = str(cell).strip().title()
                            if State.objects.filter(name=cell).exists():
                                obj = State.objects.get(name=cell)
                                obj.capital_state = True
                                obj.save()
                    except Exception as ex:
                        logger.write_to_console(str(ex),traceback, 'Import')
            else:
                for index, row in data_frame.iterrows():
                    try:
                        stripped_continent = str(row['Continent']).strip().title()
                        if Continent.objects.filter(name=stripped_continent).exists():
                            continent = (Continent.objects.get(name=stripped_continent)).id
                            name = str(row['Name']).title().strip()
                            if not Country.objects.filter(Q(name=name) & Q(continent_id=continent)).exists():
                                obj = Country(name=name,
                                              official_language=row['Official_Language'],
                                              country_code=row['Country_Code'],
                                              iso_code=row['ISO_Code'],
                                              continent_id=continent)
                                obj.save()
                        else:
                            fail.append(stripped_continent)
                    except Exception as ex:
                        logger.write_to_console(str(ex),traceback, 'Import')
            if message is None:
                message = 'Imported successfully!'
        if len(fail) > 0:
            message = 'These items not found in DB '
            for item in fail:
                message += item + ','
        
        data = {
            'title': 'Import Data',
            'message': message
        }
        return render(request, 'import.html', data)
    except Exception as ex:
        logger.write_to_console(str(ex),traceback, 'Import')
        request.session['message'] = str(ex)
        return redirect('error')
    finally:
        if full_filename is not None:
            os.remove(full_filename)
