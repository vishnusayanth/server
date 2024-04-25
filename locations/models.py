from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q


class Continent(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=50)
    official_language = models.CharField(max_length=50)
    country_code = models.IntegerField(default=None, null=True, blank=True)
    iso_code = models.CharField(max_length=10)
    continent = models.ForeignKey(Continent, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def capital(self):
        return str(State.objects.filter(Q(country=self) & Q(capital_state=True)).first())


class State(models.Model):
    name = models.CharField(max_length=50)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    capital_state = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.capital_state:
            capitals = len(State.objects.filter(Q(country_id=self.country.id) & Q(capital_state=True)))
            if capitals > 1:
                raise ValidationError('Capital already set for this country!')
        super(State, self).save(*args, **kwargs)
