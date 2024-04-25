from django.conf import settings as django_settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from server import settings

urlpatterns = [
                  path('', include('base.urls')),
                  path('dashboard/', include('locations.urls')),
                  path('api/', include('api.urls')),
                  path('web/', include('scrape.urls')),
                  path('spotify/', include('spotify.urls')),
                  path('administrator-panel/', admin.site.urls),
                  path('oauth/', include('social_django.urls', namespace='social')),
    ]+ static(settings.STATIC_URL, document_root=django_settings.STATIC_ROOT) \
              + static(django_settings.MEDIA_URL, document_root=django_settings.MEDIA_ROOT)
