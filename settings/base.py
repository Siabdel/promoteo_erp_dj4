#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This file is part of the prometeo project.

This program is free software: you can redistribute it and/or modify it 
under the terms of the GNU Lesser General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
"""

__author__ = 'Emanuele Bertoldi <emanuele.bertoldi@gmail.com>'
__copyright__ = 'Copyright (c) 2011 Emanuele Bertoldi'
__version__ = '0.0.5'

import os
import datetime
from pathlib import Path
from datetime import timedelta

from pytz import common_timezones

from django.utils.translation import gettext as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = repertoire racine au meme niveau manage.py
BASE_DIR = Path(__file__).resolve().parent.parent
#

PROJECT_PATH = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir))
THEME_PATH = os.path.join(PROJECT_PATH, 'themes', 'default')
REPORT_PATH = os.path.join(PROJECT_PATH, 'reports', 'default')

DEBUG = True

ALLOWED_HOSTS = []

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS
# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONES = [(tz, tz) for tz in common_timezones]

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'UTC'
#TIME_ZONE = 'GMT'


USE_TZ = True


SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# A tuple of directories where Django looks for translation files.
# Paths to locale directories
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
    os.path.join(PROJECT_PATH, 'settings', 'locale'),
    os.path.join(THEME_PATH, 'locale'),
    os.path.join(REPORT_PATH, 'locale'),
)

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = PROJECT_PATH + '/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/files/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = PROJECT_PATH + '/static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    THEME_PATH + '/static/',
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'Bismi ALLAH*7n%@x9c-#f6qn0@(t&7vrx-ddk8fel8fs3xx27wu+dul4rppf'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Ajustez selon votre structure de projet
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [ 
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

            ],
            # Si vous avez besoin de spécifier des loaders personnalisés, vous pouvez le faire ici :
            # 'loaders': [
            #     'django.template.loaders.filesystem.Loader',
            #     'django.template.loaders.app_directories.Loader',
            #     # Ajoutez vos loaders personnalisés ici
            # ],
        },
    }
]


# List of middleware classes to use.  Order is important; in the request phase,
# this middleware classes will be applied in the order given, and in the
# response phase the middleware will be applied in reverse order.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",  # new
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    # Add the account middleware:
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'allauth.account.middleware.AccountMiddleware',  # Ajoutez cette ligne
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # debug 
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # ... autres middlewares ...
    #'django.middleware.locale.LocaleMiddleware',
    #'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    #'core.middleware.MobileDetectionMiddleware',
    #'core.middleware.AjaxRedirectMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]


# Root for URL dispatcher.
ROOT_URLCONF = PROJECT_PATH.split(os.sep)[-1] + '.urls'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# List of search path for templates.
TEMPLATE_DIRS = (
    (os.path.join(THEME_PATH, "templates")),
    (os.path.join(REPORT_PATH, "templates")),
)

# List of installed applications.
INSTALLED_APPS = (
    # contribs
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework', # new
    # debug tools
    'debug_toolbar',
    # D- 3 rd party apps Django Rest Framework 
    'corsheaders', 
    # User Authentication
    'allauth',
    'allauth.account',
    #'allauth.socialaccount',
    # Third party
    'crispy_forms',  # Optionnel, pour les formulaires stylisés
    #'crispy_bootstrap5',  # Si vous utilisez Bootstrap 5
    "crispy_bootstrap4",
    "django_extensions",
    
    'django.contrib.admindocs',
    'fluent_comments',
    'django_comments_xtd',
    'django_comments',
    'django.contrib.redirects',
    #
    'markdownx',
    #'south',

    'core',
    'core.filebrowser',
    'core.widgets',
    'core.menus',
    'core.taxonomy',
    #'core.auth',
    #'core.registration',
    #'core.notifications',
    #'core.calendar',
    # locals 
    #'todo',
    #'addressing',
    #'partners',
    #'documents',
    #'products',
    #'stock',
    #'hr',
    #'sales',
    #'projects',
    #'knowledge',
)

# Auto-discovering of application specific settings.
for app in INSTALLED_APPS:
    try:
        prefix, sep, app_name = app.rpartition('.')
        settings = __import__(app_name, globals(), locals(), ['*'], 1)
        for attr in dir(settings):
            if not attr.startswith('_'):
                globals()[attr] = getattr(settings, attr)
    except:
        pass

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# 

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators
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