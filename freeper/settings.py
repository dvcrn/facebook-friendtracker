"""
Django settings for freeper project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import dj_mongohq_url
from datetime import datetime
from dateutil.relativedelta import relativedelta

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = "freepr"
AWS_QUERYSTRING_AUTH = False

date_after_month = datetime.today() + relativedelta(months=1)
AWS_HEADERS = {
    'Expires': date_after_month.strftime('%a, %d %b %Y %T GMT'),
    'Cache-Control': 'max-age=2419200',
}

DEFAULT_FILE_STORAGE = 'freeper.s3utils.MediaRootS3BotoStorage'
STATICFILES_STORAGE = 'freeper.s3utils.StaticRootS3BotoStorage'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '50b5e)rz=sm-m7@_buvh$5_d6(@py6h57k^gy$c&wq)gj)gv0)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = DEBUG = bool(os.environ.get('DJANGO_DEBUG', ''))
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = [
    'friendtrackr.herokuapp.com'
]

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'web',
    'api'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'freeper.urls'

WSGI_APPLICATION = 'freeper.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {'default': dj_mongohq_url.parse(os.environ.get('MONGOHQ_URL'))}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = 'https://freepr.s3.amazonaws.com/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

FACEBOOK_APP_ID = os.environ.get('FACEBOOK_APP_ID', '')
FACEBOOK_APP_SECRET = os.environ.get('FACEBOOK_APP_SECRET', '')
FACEBOOK_CANVAS_URL = 'https://apps.facebook.com/freeper/'
X_FRAME_OPTIONS = 'allow-from apps.facebook.com'

try:
    from settings_dev import *
except ImportError: pass