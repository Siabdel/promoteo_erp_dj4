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

urlpatterns = patterns('.core.menus.views',

    url(r'^users/(?P<username>[\w\d\@\.\+\-\_]+)/bookmarks/$', view='bookmark_list', name='bookmark_list'),
    url(r'^users/(?P<username>[\w\d\@\.\+\-\_]+)/bookmarks/add/$', view='bookmark_add', name='bookmark_add'),
    url(r'^users/(?P<username>[\w\d\@\.\+\-\_]+)/bookmarks/(?P<slug>[-\w]+)/edit/$', view='bookmark_edit', name='bookmark_edit'),
    url(r'^users/(?P<username>[\w\d\@\.\+\-\_]+)/bookmarks/(?P<slug>[-\w]+)/delete/$', view='bookmark_delete', name='bookmark_delete'),
)
