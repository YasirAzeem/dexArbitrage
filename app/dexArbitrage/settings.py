"""
Django settings for dexArbitrage project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
from celery.schedules import crontab

import environ


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
# APPS_DIR = ROOT_DIR / "app"

env = environ.Env()

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(ROOT_DIR / ".env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-eth_3&cr2p9ao*$kl=otal)fhjvo_m1&(-m69*qy3p@gulpnkt"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DJANGO_DEBUG", False)

ALLOWED_HOSTS = ['127.0.0.1', '0.0.0.0' 'localhost','178.18.249.12']
INTERNAL_IPS = [
    "127.0.0.1", "0.0.0.0"
]

# Application definition
TAILWIND_APP_NAME = "theme"
NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"
INSTALLED_APPS = [
    'tailwind',
    'django_browser_reload',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    'whitenoise.runserver_nostatic',
    "django.contrib.staticfiles",
    'django_celery_beat',
    'theme',
    "dexArbitrage",
    "django.contrib.humanize"
    
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
     "django_browser_reload.middleware.BrowserReloadMiddleware"
]

ROOT_URLCONF = "dexArbitrage.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "dexArbitrage.wsgi.application"


# Celery
CELERY_BROKER_URL = 'redis://localhost:6379'
# CELERY_TIMEZONE = 'UTC'
CELERY_BEAT_SCHEDULE = {
    "UpdatePrices": {
        'task': 'dexArbitrage.tasks.priceWork',
        'schedule': 150 #crontab(minute="*/1")  # Every 1 min
    },
        "UpdateDeals": {
        'task': 'dexArbitrage.tasks.dealWork',
        'schedule': 20 #crontab(minute="*/1")  # Every 1 min
    }
}


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }
DATABASES = {"default": env.db("DATABASE_URL")}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

import os
# STATIC_URL = '/static/' 
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "static"),
# ]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATIC_URL = '/static/'

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
