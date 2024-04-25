import os
from pathlib import Path
from sshtunnel import SSHTunnelForwarder

from server.config import GITHUB_SECRET, GITHUB_KEY, DB_HOST, DB_PASSWORD, DB_USER, \
    DB_NAME, DJANGO_APP_KEY, ALLOWED_HOST, DEBUG_MODE, PRODUCTION, BASE_DIR,DB_PORT, LOCAL_DB

SECRET_KEY = DJANGO_APP_KEY

# 2 Flags are used to enable DEBUG in production.
DEBUG = DEBUG_MODE
if PRODUCTION:
    ALLOWED_HOSTS = [ALLOWED_HOST]
else:
    ALLOWED_HOSTS = []

CORS_ORIGIN_ALLOW_ALL = True

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api.apps.ApiConfig',
    'spotify.apps.SpotifyConfig',
    'base.apps.BaseConfig',
    'locations.apps.LocationsConfig',
    'scrape.apps.ScrapeConfig',
    'rest_framework.authtoken',
    'rest_framework',
    'social_django',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    "server.utils.CustomRequestMiddleware"
]

ROOT_URLCONF = 'server.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
                'server.utils.custom_context',
            ],
        },
    },
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework.authentication.TokenAuthentication',),
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}

WSGI_APPLICATION = 'server.wsgi.application'

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

if LOCAL_DB:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3'
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'vishnusayanth$' + DB_NAME,
            'USER': DB_USER,
            'PASSWORD': DB_PASSWORD,
            'HOST': DB_HOST,
            'PORT': DB_PORT,
        }
    }
AUTH_USER_MODEL = 'base.Developer'

SOCIAL_AUTH_USER_MODEL = 'base.Developer'
SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['username']
SOCIAL_AUTH_GITHUB_KEY = GITHUB_KEY
SOCIAL_AUTH_GITHUB_SECRET = GITHUB_SECRET
SOCIAL_AUTH_GITHUB_SCOPE = ['username']
SOCIAL_AUTH_GITHUB_PROFILE_EXTRA_PARAMS = {
    'fields': 'id,username',
}
SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'server.utils.cleanup_social_account',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)


AUTHENTICATION_BACKENDS = (
    'social_core.backends.github.GithubOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = '/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'
if PRODUCTION:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
else:
    STATICFILES_DIRS = [
            os.path.join(BASE_DIR, "static"),
        ]

