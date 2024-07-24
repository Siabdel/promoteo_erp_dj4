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

from django.db.models.signals import post_migrate
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group

from .core.auth.models import MyPermission
from core.utils import check_dependency
from core.menus.models import *
from .core.notifications.models import Signature
from core.widgets.models import *

check_dependency('core.widgets')
check_dependency('.core.menus')
check_dependency('.core.taxonomy')
check_dependency('.core.auth')

def install(sender, **kwargs):
    main_menu, is_new = Menu.objects.get_or_create(slug="main")
    users_group, is_new = Group.objects.get_or_create(name=_('Users'))

    # Menus.
    todo_menu, is_new = Menu.objects.get_or_create(
        slug="todo_menu",
        description=_("Main menu for tasks")
    )
    
    # Links.
    tasks_link, is_new = Link.objects.get_or_create(
        title=_("Tasks"),
        slug="tasks",
        description=_("List of tasks"),
        url="{% url task_list %}",
        submenu=todo_menu,
        menu=main_menu
    )

    planned_tasks_link, is_new = Link.objects.get_or_create(
        title=_("Planned"),
        slug="planned_tasks",
        url="{% url task_list %}",
        menu=todo_menu
    )

    unplanned_tasks_link, is_new = Link.objects.get_or_create(
        title=_("Unplanned"),
        slug="unplanned_tasks",
        url="{% url unplanned_task_list %}",
        menu=todo_menu
    )

    # Signatures.
    task_created_signature, is_new = Signature.objects.get_or_create(
        title=_("Task created"),
        slug="task-created"
    )

    task_changed_signature, is_new = Signature.objects.get_or_create(
        title=_("Task changed"),
        slug="task-changed"
    )

    task_deleted_signature, is_new = Signature.objects.get_or_create(
        title=_("Task deleted"),
        slug="task-deleted"
    )

    # Permissions.
    can_view_task, is_new = MyPermission.objects.get_or_create_by_natural_key("view_task", "todo", "task")
    can_add_task, is_new = MyPermission.objects.get_or_create_by_natural_key("add_task", "todo", "task")

    users_group.permissions.add(can_view_task, can_add_task)

    tasks_link.only_with_perms.add(can_view_task)

    # Widgets.
    latest_tasks_widget_template, is_new = WidgetTemplate.objects.get_or_create(
        title=_("Latest tasks"),
        slug="tasks-widget-template",
        description=_("It renders the list of the latest tasks."),
        source="prometeo.todo.widgets.latest_tasks",
        template_name="todo/widgets/latest_tasks.html",
    )

    latest_planned_tasks_widget_template, is_new = WidgetTemplate.objects.get_or_create(
        title=_("Latest planned tasks"),
        slug="planned-tasks-widget-template",
        description=_("It renders the list of the latest planned tasks."),
        source="prometeo.todo.widgets.latest_planned_tasks",
        template_name="todo/widgets/latest_tasks.html",
    )

    latest_unplanned_tasks_widget_template, is_new = WidgetTemplate.objects.get_or_create(
        title=_("Latest unplanned tasks"),
        slug="unplanned-tasks-widget-template",
        description=_("It renders the list of the latest unplanned tasks."),
        source="prometeo.todo.widgets.latest_unplanned_tasks",
        template_name="todo/widgets/latest_tasks.html",
    )

    today_tasks_widget_template, is_new = WidgetTemplate.objects.get_or_create(
        title=_("Today tasks"),
        slug="today-tasks-widget-template",
        description=_("It renders the list of the today tasks."),
        source="prometeo.todo.widgets.today_tasks",
        template_name="todo/widgets/latest_tasks.html",
    )

post_migrate.connect(install, dispatch_uid="install_todo")
