"""
Django's settings for movie_mania project.

Generated by 'django-auth startproject' using Django 3.2.13.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    with open(os.path.join(BASE_DIR, '.moviesenv')) as file:
        MOVIE_ENV = json.load(file)
except FileNotFoundError:
    MOVIE_ENV = {
        'DATABASE': {}
    }

SECRET_KEY = 'django-insecure-_r!%!9%g=+wc5!(vodsw95%ls&$*ti)r2aub6r5nh(nu@bu_e8'

BASE_URL = MOVIE_ENV.get('BASE_URL', '')
ENV = MOVIE_ENV.get('ENV', 'dev').lower()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = MOVIE_ENV.get('DEBUG', False)

ALLOWED_HOSTS = MOVIE_ENV.get('HOST_IP')
CORS_ORIGIN_ALLOW_ALL = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'corsheaders',
    'movies'
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
    'movie_mania.middleware.request.LoggingMiddleware',
]

ROOT_URLCONF = 'movie_mania.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'movie_mania.wsgi.application'

# Database

DATABASES = {
    'default': MOVIE_ENV['DATABASE'],
}

# https://docs.djangoproject.com/en/3.2/ref/settings/#databases


REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'movie_mania.middleware.exceptions.drf_exception_handler',

    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FormParser',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    )
}

DATE_INPUT_FORMATS = '%Y-%m-%d %H:%M'
DATE_OUTPUT_FORMATS = '%Y-%m-%d %H:%M'

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_URL = '/static/'

STATICFILES_DIRS = [os.path.join(os.path.dirname(BASE_DIR), 'backend', 'templates', 'static')]
STATIC_ROOT = os.path.abspath(os.path.join(os.path.dirname(BASE_DIR), 'static'))

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
