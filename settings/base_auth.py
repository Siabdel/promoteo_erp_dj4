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

from base import DEBUG, TEMPLATE_CONTEXT_PROCESSORS, MIDDLEWARE_CLASSES
from django.conf import settings

AUTH_PROFILE_MODULE = 'auth.UserProfile'
# Paramètres d'authentification
AUTH_USER_MODEL = 'auth.User'  # Remplace AUTH_PROFILE_MODULE

LOGIN_URL = '/users/login'
LOGOUT_URL = '/users/logout'
LOGIN_REDIRECT_URL = '/users/logged/'

# URLs requérant une connexion
LOGIN_REQUIRED_URLS = [
    r'/(.*)$',
]

LOGIN_REQUIRED_URLS_EXCEPTIONS = [
    r'/static/(.*)$',
    r'/users/login/$',
    r'/users/register/$',
    r'/users/activate/(.*)$',
]

# Contexte des templates
if 'django.template.context_processors.request' not in settings.TEMPLATES[0]['OPTIONS']['context_processors']:
    settings.TEMPLATES[0]['OPTIONS']['context_processors'].append('django.template.context_processors.request')

settings.TEMPLATES[0]['OPTIONS']['context_processors'].append('core.auth.context_processors.auth')

# Middleware
if 'django.contrib.auth.middleware.AuthenticationMiddleware' not in settings.MIDDLEWARE:
    settings.MIDDLEWARE.append('django.contrib.auth.middleware.AuthenticationMiddleware')

settings.MIDDLEWARE.extend([
    'core.auth.middleware.RequireLoginMiddleware',
    'core.auth.middleware.LoggedInUserCacheMiddleware',
])

# Backends d'authentification
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'core.auth.backends.ObjectPermissionBackend',
]

# Configuration de l'email pour le mode debug
if settings.DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'