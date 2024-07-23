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

from django.shortcuts import render_to_response, get_object_or_404
from django.utils.translation import gettext as _
from django.views.generic import list_detail, create_update
from django.views.generic.simple import redirect_to
from django.template import RequestContext
from django.contrib import messages

from .core.auth.decorators import obj_permission_required as permission_required
from .core.views import filtered_list_detail

from ..models import *
from ..forms import *

def _get_ticket(request, *args, **kwargs):
    code = kwargs.get('code', None)
    project_code = kwargs.get('project', None)
    return get_object_or_404(Ticket, code=code, project__code=project_code)

@permission_required('projects.view_ticket') 
def ticket_list(request, project, page=0, paginate_by=5, **kwargs):
    """Displays the list of all tickets of a specified project.
    """
    project = get_object_or_404(Project, code=project)
    return filtered_list_detail(
        request,
        project.tickets.all(),
        fields=['code', 'title', 'parent', 'author', 'manager', 'created', 'closed', 'urgency', 'status'],
        paginate_by=paginate_by,
        page=page,
        extra_context={
            'object': project,
        },
        **kwargs
    )

@permission_required('projects.view_ticket', _get_ticket)    
def ticket_detail(request, project, code, **kwargs):
    """Show ticket details.
    """
    project = get_object_or_404(Project, code=project)
    ticket = get_object_or_404(Ticket, project=project, code=code)
    object_list = project.tickets.all()
    return list_detail.object_detail(
        request,
        object_id=ticket.pk,
        queryset=object_list,
        extra_context={'object_list': object_list},
        **kwargs
    )

@permission_required('projects.add_ticket')     
def ticket_add(request, project, milestone=None, **kwargs):
    """Adds a new ticket.
    """
    project = get_object_or_404(Project, code=project)
    ticket = Ticket(project=project, author=request.user)

    initial = {}

    if milestone is not None:
        milestone = get_object_or_404(Milestone, code=milestone, project=project)
        initial['milestone'] = milestone

    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket, initial=initial)
        if form.is_valid():
            ticket = form.save()
            messages.success(request, _("Your ticket has been registered."))
            return redirect_to(request, url=ticket.get_absolute_url())
    else:
        form = TicketForm(instance=ticket, initial=initial)

    if not request.user.has_perm("projects.change_milestone"):
        del form.fields['milestone']

    if not request.user.has_perm("projects.change_assignee"):
        del form.fields['assignee']

    return render_to_response('projects/ticket_edit.html', RequestContext(request, {'form': form, 'object': ticket}))

@permission_required('projects.change_ticket', _get_ticket)     
def ticket_edit(request, project, code, **kwargs):
    """Edits a ticket.
    """
    project = get_object_or_404(Project, code=project)
    ticket = get_object_or_404(Ticket, project=project, code=code)
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            ticket = form.save()
            messages.success(request, _("The ticket was updated successfully."))
            return redirect_to(request, url=ticket.get_absolute_url())
    else:
        form = TicketForm(instance=ticket)

    if not request.user.has_perm("projects.change_milestone"):
        del form.fields['milestone']

    if not request.user.has_perm("projects.change_assignee"):
        del form.fields['assignee']

    return render_to_response('projects/ticket_edit.html', RequestContext(request, {'form': form, 'object': ticket}))

@permission_required('projects.delete_ticket', _get_ticket)     
def ticket_delete(request, project, code, **kwargs):
    """Deletes a ticket.
    """
    project = get_object_or_404(Project, code=project)
    ticket = get_object_or_404(Ticket, project=project, code=code)
    return create_update.delete_object(
        request,
        model=Ticket,
        object_id=ticket.pk,
        post_delete_redirect='/projects/%s/tickets' % project.code,
        template_name='projects/ticket_delete.html',
        **kwargs
    )
