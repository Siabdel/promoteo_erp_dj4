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
     
import re

from django.conf import settings  
from django.contrib.auth.decorators import login_required

from .core.auth.cache import LoggedInUserCache

# Inspired by http://www.djangosnippets.org/snippets/1220/

class RequireLoginMiddleware(object):
    """
    Middleware component that wraps the login_required decorator around 
    matching URL patterns. To use, add the class to MIDDLEWARE_CLASSES and 
    define LOGIN_REQUIRED_URLS and LOGIN_REQUIRED_URLS_EXCEPTIONS in your 
    settings.py. For example:
    ------
    LOGIN_REQUIRED_URLS = (
        r'/topsecret/(.*)$',
    )
    LOGIN_REQUIRED_URLS_EXCEPTIONS = (
        r'/topsecret/login(.*)$', 
        r'/topsecret/logout(.*)$',
    )
    ------                 
    LOGIN_REQUIRED_URLS is where you define URL patterns; each pattern must 
    be a valid regex.     
    
    LOGIN_REQUIRED_URLS_EXCEPTIONS is, conversely, where you explicitly 
    define any exceptions (like login and logout URLs).
    """
    def __init__(self):
        self.required = tuple([re.compile(url) for url in settings.LOGIN_REQUIRED_URLS])
        self.exceptions = tuple([re.compile(url) for url in settings.LOGIN_REQUIRED_URLS_EXCEPTIONS])
    
    def process_view(self,request,view_func,view_args,view_kwargs):
        # No need to process URLs if user already logged in
        if request.user.is_authenticated(): return None
        # An exception match should immediately return None
        for url in self.exceptions:
            if url.match(request.path): return None
        # Requests matching a restricted URL pattern are returned 
        # wrapped with the login_required decorator
        for url in self.required:
            if url.match(request.path): return login_required(view_func)(request,*view_args,**view_kwargs)
        # Explicitly return None for all non-matching requests
        return None

# Inspired by http://stackoverflow.com/a/7469395/1063729

class LoggedInUserCacheMiddleware(object):
    """Initialize the user attribute of the LoggedInUserCache class.
    """
    def process_request(self, request):
        logged_in_user = LoggedInUserCache()
        logged_in_user.set_user(request)

        return None

