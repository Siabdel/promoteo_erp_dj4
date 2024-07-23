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

urlpatterns = patterns('.core.taxonomy.views',

    # Search.
    url(r'^search/$', view='search', name='search'),
    url(r'^search/(?P<query_string>.+)/$', view='search', name='search_with_query'),

    # Categories.
    url(r'^categories/$', view='category_list', name='category_list'),
    url(r'^categories/add/$', view='category_add', name='category_add'),
    url(r'^categories/(?P<slug>[-\w]+)/$', view='category_detail', name='category_detail'),
    url(r'^categories/(?P<slug>[-\w]+)/edit/$', view='category_edit', name='category_edit'),
    url(r'^categories/(?P<slug>[-\w]+)/delete/$', view='category_delete', name='category_delete'),

    # Tags.
    url(r'^tags/$', view='tag_list', name='tag_list'),
    url(r'^tags/add/$', view='tag_add', name='tag_add'),
    url(r'^tags/(?P<slug>[-\w]+)/$', view='tag_detail', name='tag_detail'),
    url(r'^tags/(?P<slug>[-\w]+)/edit/$', view='tag_edit', name='tag_edit'),
    url(r'^tags/(?P<slug>[-\w]+)/delete/$', view='tag_delete', name='tag_delete'),
)
