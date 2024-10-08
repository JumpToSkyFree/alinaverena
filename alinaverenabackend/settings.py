"""
Django settings for alinaverenabackend project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

# TODO: Tutorial deployment of django https://realpython.com/django-nginx-gunicorn/#turning-on-https
# TODO: https://github.com/django-parler/django-parler-rest
# TODO: https://www.youtube.com/watch?v=f0hdXr2MOEA&ab_channel=DanielRoyGreenfeld
# TODO: https://www.iditect.com/faq/python/nginx-is-throwing-an-403-forbidden-on-static-files.html

from pathlib import Path
import environ
import os

env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# This is the environment varialbes file.
environ.Env.read_env(BASE_DIR / '.env')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-yopy%lp-aq0jp_qz8*%m4v(l%+qelh6=%vqqy5y(b^i48=x0#)'
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG') == 'on'

ALLOWED_HOSTS = ['localhost', '127.0.0.1'] if DEBUG else [env('SERVER_ADDRESS'), 'localhost', '127.0.0.1', '.alinaverena.com']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'parler',
    'corsheaders',
    'alinaverenaapi'
]

MIDDLEWARE = [
    'alinaverenaapi.middleware.UserIPAddressRegistrationMiddleware',
    'alinaverenaapi.middleware.ClientWebsiteAccessMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'alinaverenabackend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
            BASE_DIR / 'staticfiles'
        ],
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

WSGI_APPLICATION = 'alinaverenabackend.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DATABASE_NAME') if not DEBUG else 'alinaverenadb',
        'USER': env('DATABASE_USER') if not DEBUG else 'alina',
        'PASSWORD': env('DATABASE_PASSWORD') if not DEBUG else 'alinaverena',
        'HOST': env('DATABASE_HOST') if not DEBUG else '127.0.0.1',
        'PORT': env('DATABASE_PORT') if not DEBUG else '5432'
    }
}

# CACHES = {
#     "default": {
#         "BACKEND": "django.core.cache.backends.db.DatabaseCache",
#         "LOCATION": "api_cache"
#     }
# }

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/


TELEGRAM_ACTIVITY_BOT_KEY = '6687658372:AAGIouVKweafjYXTT6gcrhNqDoNz-UqrtTw'
TELEGRAM_CHAT_ID = -1002082051233


STATIC_URL = 'static/'

STATIC_ROOT = 'static/' if DEBUG else env('STATIC_ROOT')

STATICFILES_DIRS = [
        BASE_DIR / 'staticfiles'
]


MEDIA_URL = 'media/'
MEDIA_ROOT = 'media/' if DEBUG else env('MEDIA_ROOT')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_ALL_ORIGINS = True if not DEBUG else False
CORS_ALLOW_CREDENTIALS = True if not DEBUG else False
SECURE_CROSS_ORIGIN_OPENER_POLICY = True

# CORS_ALLOWED_ORIGINS = ['http://localhost:5173']

CURRENCIES_FILE_PATH = 'alinaverenaapi'
COUNTRIES_FILE_PATH = 'alinaverenaapi'
LANGUAGES_FILE_PATH = 'alinaverenaapi'

AUTH_USER_MODEL = 'alinaverenaapi.Client'

SITE_ID = 1

PARLER_LANGUAGES = {
    SITE_ID: (
        {'code': 'en', },
        {'code': 'ru', },
        {'code': 'fr', }
    ),
    'default': {
        # defaults to PARLER_DEFAULT_LANGUAGE_CODE
        'fallbacks': ['en'],
        # the default; let .active_translations() return fallbacks too.
        'hide_untranslated': False,
    }
}

REST_FRAMEWORK = {
    # 'DEFAULT_PERMISSION_CLASSES': (
    #     'rest_framework.permissions.IsAuthenticated',
    # ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    )
}

if not DEBUG:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
            },
        },
        "root": {
            "handlers": ["console"],
            "level": "WARNING",
        },
        "loggers": {
            "django": {
                "handlers": ["console"],
                "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
                "propagate": False,
            },
        },
    }