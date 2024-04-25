from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext as _

from base import models


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['username']

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'url', 'password1', 'password2')
        }),
    )

    fieldsets = (
        (None, {'fields': ('username', 'url', 'password')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )


admin.site.register(models.Developer, UserAdmin)
admin.site.register(models.RequestCounter)
admin.site.unregister(Group)
