from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

from locations.models import State


class UserManager(BaseUserManager):

    def create_user(self, username, password=None, **extra_fields):
        """Creates and saves a new User"""
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, password, email=None):
        """Creates and saves a new super user"""
        user = self.create_user(username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        return user


class Developer(AbstractBaseUser, PermissionsMixin):
    """Custom user model"""
    username = models.CharField(max_length=20, default=None, unique=True)
    email = models.EmailField(default=None, null=True, blank=True)
    url = models.CharField(max_length=200, default=None, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'username'


class RequestCounter(models.Model):
    count = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if len(RequestCounter.objects.all()) > 1:
            raise Exception('This class cannot have more than one object!')
        super(RequestCounter, self).save(*args, **kwargs)
