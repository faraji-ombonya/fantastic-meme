"""
Django settings for PROJECT project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from decouple import config


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-pg(id^+b8d)+gh5^983z-%4^=+h!p#0=h4$t$0=8ogd1_9ks^8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'spider',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'PROJECT.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'PROJECT.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Telegram
TELEGRAM_CHAT_ID = config('TELEGRAM_CHAT_ID', None)
TELEGRAM_API_KEY = config('TELEGRAM_API_KEY', None)
TELEGRAM_BASE_URL = config('TELEGRAM_BASE_URL', None)
TELEGRAM_SPORTS_KENYA_CHAT_ID = config('TELEGRAM_SPORTS_KENYA_CHAT_ID', None)
TELEGRAM_KENYAN_POLITICS_CHAT_ID = config(
    'TELEGRAM_KENYAN_POLITICS_CHAT_ID', None)
TELEGRAM_TEST_CHANNEL_CHAT_ID = config('TELEGRAM_TEST_CHANNEL_CHAT_ID', None)

# The Standard
STANDARD_SPORTS_URL = config('STANDARD_SPORTS_URL', None)
STANDARD_POLITICS_URL = config('STANDARD_POLITICS_URL', None)

# The Star
STAR_BASE_URL = config('STAR_BASE_URL', None)
STAR_SPORTS_URL = config('STAR_SPORTS_URL', None)
STAR_SPORTS_FOOTBALL_URL = config('STAR_SPORTS_FOOTBALL_URL', None)
STAR_SPORTS_ATHLETICS_URL = config('STAR_SPORTS_ATHLETICS_URL', None)
STAR_SPORTS_RUGBY_URL = config('STAR_SPORTS_RUGBY_URL', None)
STAR_SPORTS_TENNIS_URL = config('STAR_SPORTS_TENNIS_URL', None)
STAR_SPORTS_GOLF_URL = config('STAR_SPORTS_GOLF_URL', None)
STAR_SPORTS_BOXING_URL = config('STAR_SPORTS_BOXING_URL', None)
STAR_SPORTS_BASKETBALL_URL = config('STAR_SPORTS_BASKETBALL_URL', None)
STAR_POLITICS_URL = config('STAR_POLITICS_URL', None)


# X
X_API_KEY = config("X_API_KEY", None)
X_API_KEY_SECRET = config("X_API_KEY_SECRET", None)
X_BEARER_TOKEN = config("X_BEARER_TOKEN", None)
X_ACCESS_TOKEN = config("X_ACCESS_TOKEN", None)
X_ACCESS_TOKEN_SECRET = config("X_ACCESS_TOKEN_SECRET", None)
