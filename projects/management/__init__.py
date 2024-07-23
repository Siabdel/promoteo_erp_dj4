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

from django.urls import reverse
from django.db.models.signals import post_migrate
from django.utils.translation import gettext as _
from django.contrib.auth.models import Group

from .core.auth.models import MyPermission
from core.utils import check_dependency
from core.menus.models import *
from .core.notifications.models import Signature

check_dependency('core.widgets')
check_dependency('.core.menus')
check_dependency('.core.taxonomy')
check_dependency('.core.auth')
check_dependency('prometeo.todo')

def install(sender, **kwargs):
    main_menu, is_new = Menu.objects.get_or_create(slug="main")
    users_group, is_new = Group.objects.get_or_create(name=_('Users'))
    employees_group, is_new = Group.objects.get_or_create(name=_('Employees'))

    # Menus.
    project_menu, is_new = Menu.objects.get_or_create(
        slug="project-menu",
        description=_("Main menu for projects")
    )

    milestone_menu, is_new = Menu.objects.get_or_create(
        slug="milestone-menu",
        description=_("Main menu for milestones")
    )

    ticket_menu, is_new = Menu.objects.get_or_create(
        slug="ticket-menu",
        description=_("Main menu for tickets")
    )
    
    # Links.
    projects_link, is_new = Link.objects.get_or_create(
        title=_("Projects"),
        slug="projects",
        description=_("Project management"),
        url=reverse("project_list"),
        menu=main_menu
    )

    project_details_link, is_new = Link.objects.get_or_create(
        title=_("Details"),
        slug="project-details",
        url="{{ object.get_absolute_url }}",
        menu=project_menu
    )

    project_milestones_link, is_new = Link.objects.get_or_create(
        title=_("Milestones"),
        slug="project-milestones",
        url="{% url milestone_list object.code %}",
        menu=project_menu
    )

    project_tickets_link, is_new = Link.objects.get_or_create(
        title=_("Tickets"),
        slug="project-tickets",
        url="{% url ticket_list object.code %}",
        menu=project_menu
    )

    project_timeline_link, is_new = Link.objects.get_or_create(
        title=_("Timeline"),
        slug="project-timeline",
        url="{% url project_timeline object.code %}",
        menu=project_menu
    )

    milestone_details_link, is_new = Link.objects.get_or_create(
        title=_("Details"),
        slug="milestone-details",
        url="{{ object.get_absolute_url }}",
        menu=milestone_menu
    )

    milestone_tickets_link, is_new = Link.objects.get_or_create(
        title=_("Tickets"),
        slug="milestone-tickets",
        url="{% url milestone_tickets object.project.code object.code %}",
        menu=milestone_menu
    )

    milestone_timeline_link, is_new = Link.objects.get_or_create(
        title=_("Timeline"),
        slug="milestone-timeline",
        url="{% url milestone_timeline object.project.code object.code %}",
        menu=milestone_menu
    )

    ticket_details_link, is_new = Link.objects.get_or_create(
        title=_("Details"),
        slug="ticket-details",
        url="{{ object.get_absolute_url }}",
        menu=ticket_menu
    )

    ticket_tasks_link, is_new = Link.objects.get_or_create(
        title=_("Tasks"),
        slug="ticket-tasks",
        url="{% url ticket_tasks object.project.code object.code %}",
        menu=ticket_menu
    )

    ticket_timeline_link, is_new = Link.objects.get_or_create(
        title=_("Timeline"),
        slug="ticket-timeline",
        url="{% url ticket_timeline object.project.code object.code %}",
        menu=ticket_menu
    )

    # Signatures.
    project_created_signature, is_new = Signature.objects.get_or_create(
        title=_("Project created"),
        slug="project-created"
    )

    project_changed_signature, is_new = Signature.objects.get_or_create(
        title=_("Project changed"),
        slug="project-changed"
    )

    project_deleted_signature, is_new = Signature.objects.get_or_create(
        title=_("Project deleted"),
        slug="project-deleted"
    )

    milestone_created_signature, is_new = Signature.objects.get_or_create(
        title=_("Milestone created"),
        slug="milestone-created"
    )

    milestone_changed_signature, is_new = Signature.objects.get_or_create(
        title=_("Milestone changed"),
        slug="milestone-changed"
    )

    milestone_deleted_signature, is_new = Signature.objects.get_or_create(
        title=_("Milestone deleted"),
        slug="milestone-deleted"
    )

    ticket_created_signature, is_new = Signature.objects.get_or_create(
        title=_("Ticket created"),
        slug="ticket-created"
    )

    ticket_changed_signature, is_new = Signature.objects.get_or_create(
        title=_("Ticket changed"),
        slug="ticket-changed"
    )

    ticket_deleted_signature, is_new = Signature.objects.get_or_create(
        title=_("Ticket deleted"),
        slug="ticket-deleted"
    )

    # Permissions.
    can_view_project, is_new = MyPermission.objects.get_or_create_by_natural_key("view_project", "projects", "project")
    can_add_project, is_new = MyPermission.objects.get_or_create_by_natural_key("add_project", "projects", "project")
    can_view_milestone, is_new = MyPermission.objects.get_or_create_by_natural_key("view_milestone", "projects", "milestone")
    can_add_milestone, is_new = MyPermission.objects.get_or_create_by_natural_key("add_milestone", "projects", "milestone")
    can_view_ticket, is_new = MyPermission.objects.get_or_create_by_natural_key("view_ticket", "projects", "ticket")
    can_add_ticket, is_new = MyPermission.objects.get_or_create_by_natural_key("add_ticket", "projects", "ticket")

    projects_link.only_with_perms.add(can_view_project)

    employees_group.permissions.add(can_add_project, can_add_milestone)
    users_group.permissions.add(can_view_project, can_view_milestone, can_view_ticket, can_add_ticket)

post_migrate.connect(install, dispatch_uid="install_projects")
