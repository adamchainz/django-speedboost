# -*- coding:utf-8 -*-
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DEBUG = True
TEMPLATE_DEBUG = DEBUG

SECRET_KEY = 'THISuISdNOT9A$SECRET9x&ji!vceayg+wwt472!bgs$0!i3k4'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_speedboost',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        'OPTIONS': {'charset': 'utf8mb4'},
        'TEST': {
            'COLLATION': "utf8mb4_general_ci",
            'CHARSET': "utf8mb4"
        }
    }
}

ALLOWED_HOSTS = []

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_speedboost',
    'testapp'
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'urls'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
STATIC_URL = '/static/'

try:
    from local_settings import *  # noqa
except ImportError:
    pass

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [],
        },
    },
]
