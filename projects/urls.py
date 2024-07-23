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

urlpatterns = patterns('projects.views',

    # Projects.
    url(r'^projects/$', view='projects.project_list', name='project_list'),
    url(r'^projects/add/$', view='projects.project_add', name='project_add'),
    url(r'^projects/(?P<code>[-\w]+)/$', view='projects.project_detail', name='project_detail'),
    url(r'^projects/(?P<code>[-\w]+)/edit/$', view='projects.project_edit', name='project_edit'),
    url(r'^projects/(?P<code>[-\w]+)/delete/$', view='projects.project_delete', name='project_delete'),
    url(r'^projects/(?P<code>[-\w]+)/timeline/$', 'projects.project_detail', {'template_name': 'projects/project_timeline.html'}, 'project_timeline'),
    
    # Milestones.
    url(r'^projects/(?P<project>[-\w]+)/milestones/$', view='milestones.milestone_list', name='milestone_list'),
    url(r'^projects/(?P<project>[-\w]+)/milestones/add/$', view='milestones.milestone_add', name='milestone_add'),
    url(r'^projects/(?P<project>[-\w]+)/milestones/(?P<code>[-\w]+)/$', view='milestones.milestone_detail', name='milestone_detail'),
    url(r'^projects/(?P<project>[-\w]+)/milestones/(?P<code>[-\w]+)/edit/$', view='milestones.milestone_edit', name='milestone_edit'),
    url(r'^projects/(?P<project>[-\w]+)/milestones/(?P<code>[-\w]+)/delete/$', view='milestones.milestone_delete', name='milestone_delete'),
    url(r'^projects/(?P<project>[-\w]+)/milestones/(?P<code>[-\w]+)/close/$', view='milestones.milestone_close', name='milestone_close'),
    url(r'^projects/(?P<project>[-\w]+)/milestones/(?P<code>[-\w]+)/reopen/$', view='milestones.milestone_reopen', name='milestone_reopen'),
    url(r'^projects/(?P<project>[-\w]+)/milestones/(?P<code>[-\w]+)/tickets/$', view='milestones.milestone_tickets', name='milestone_tickets'),
    url(r'^projects/(?P<project>[-\w]+)/milestones/(?P<milestone>[-\w]+)/tickets/add/$', view='tickets.ticket_add', name='milestone_ticket_add'),
    url(r'^projects/(?P<project>[-\w]+)/milestones/(?P<code>[-\w]+)/timeline/$', 'milestones.milestone_detail', {'template_name': 'projects/milestone_timeline.html'}, 'milestone_timeline'),

    # Tickets.
    url(r'^projects/(?P<project>[-\w]+)/tickets/$', view='tickets.ticket_list', name='ticket_list'),
    url(r'^projects/(?P<project>[-\w]+)/tickets/add/$', view='tickets.ticket_add', name='ticket_add'),
    url(r'^projects/(?P<project>[-\w]+)/tickets/(?P<code>\d+)/$', view='tickets.ticket_detail', name='ticket_detail'),
    url(r'^projects/(?P<project>[-\w]+)/tickets/(?P<code>\d+)/edit/$', view='tickets.ticket_edit', name='ticket_edit'),
    url(r'^projects/(?P<project>[-\w]+)/tickets/(?P<code>\d+)/delete/$', view='tickets.ticket_delete', name='ticket_delete'),
    url(r'^projects/(?P<project>[-\w]+)/tickets/(?P<code>\d+)/tasks/$', 'tickets.ticket_detail', {'template_name': 'projects/ticket_tasks.html'}, 'ticket_tasks'),
    url(r'^projects/(?P<project>[-\w]+)/tickets/(?P<code>\d+)/timeline/$', 'tickets.ticket_detail', {'template_name': 'projects/ticket_timeline.html'}, 'ticket_timeline'),
)
