"""
Django settings for stud_comms project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
import django.conf.global_settings as DEFAULT_SETTINGS
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# import os, sys
# BASE_DIR = os.path.dirname(__file__)
# sys.path.insert(0, BASE_DIR)
import os
BASE_DIR = os.path.dirname(os.path.dirname((os.path.abspath(__file__))))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'f0x1nqfvxq7io4rk_!3-^g1ogf_p+$v23&+ijc10k3hn&5ep5%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    # Third Party Apps
    'debug_toolbar',
    'crispy_forms',
    'simple_history',
    'django_tables2',
    # Project Specific Apps
    'core',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Third Party middleware app(s)
    'simple_history.middleware.HistoryRequestMiddleware',
    'stud_comms.middleware.CommsMiddleware',
)

ROOT_URLCONF = 'stud_comms.urls'

WSGI_APPLICATION = 'stud_comms.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'fms_stud_comms_dev',
        'HOST': 'barbarian.ncl.ac.uk',
        'PORT': '3306',
        'USER': 'student',
        'PASSWORD': 'StudentRid1'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,  'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_SETTINGS.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
)


CRISPY_TEMPLATE_PACK = 'bootstrap3'