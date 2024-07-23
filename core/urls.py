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

from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('',

    # Home page.
    (r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'index.html'}),
    
    # Admin.
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    
    # Comments framework.
    (r'^comments/', include('django_comments.urls')),
)

urlpatterns += staticfiles_urlpatterns()

LOADING = False

def autodiscover():
    """ Auto discover urls of installed applications.
    """
    global LOADING
    if LOADING:
        return
    
    LOADING = True

    import imp
    
    for app in settings.INSTALLED_APPS:
        if app.startswith('django') \
        or app == '.core':
            continue
            
        # Step 1: find out the app's __path__.
        try:
            app_path = __import__(app, {}, {}, [app.split('.')[-1]]).__path__
        except AttributeError:
            continue

        # Step 2: use imp.find_module to find the app's urls.py.
        try:
            imp.find_module('urls', app_path)
        except ImportError:
            continue

        # Step 3: return the app's url patterns.
        pkg, sep, name = app.rpartition('.')
        global urlpatterns
        urlpatterns += patterns("", (r'^', include('%s.urls' % app)))
        
    LOADING = False
