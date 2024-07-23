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

from ..models import *

check_dependency('core.widgets')
check_dependency('.core.menus')
check_dependency('.core.taxonomy')
check_dependency('.core.auth')
check_dependency('prometeo.products')
check_dependency('prometeo.partners')
check_dependency('prometeo.documents')

def install(sender, created_models, **kwargs):
    main_menu, is_new = Menu.objects.get_or_create(slug="main")
    administrative_employees_group, is_new = Group.objects.get_or_create(name=_('Administrative Employees'))

    # Menus.
    stock_menu, is_new = Menu.objects.get_or_create(
        slug="stock_menu",
        description=_("Main menu for stock management")
    )

    warehouse_menu, is_new = Menu.objects.get_or_create(
        slug="warehouse_menu",
        description=_("Main menu for warehouse model")
    )

    deliverynote_menu, is_new = Menu.objects.get_or_create(
        slug="deliverynote_menu",
        description=_("Main menu for delivery note model")
    )
    
    # Links.
    stock_link, is_new = Link.objects.get_or_create(
        title=_("Stock"),
        slug="stock",
        description=_("Stock management"),
        url="{% if perms.stock.view_warehouse %}{% url warehouse_list %}{% else %}{% url deliverynote_list %}{% endif %}",
        submenu=stock_menu,
        menu=main_menu
    )

    warehouses_link, is_new = Link.objects.get_or_create(
        title=_("Warehouses"),
        slug="warehouse-list",
        description=_("Warehouses management"),
        url=reverse("warehouse_list"),
        menu=stock_menu
    )

    movements_link, is_new = Link.objects.get_or_create(
        title=_("Movements"),
        slug="movement-list",
        description=_("Movements management"),
        url=reverse("movement_list"),
        menu=stock_menu
    )

    deliverynotes_link, is_new = Link.objects.get_or_create(
        title=_("Delivery notes"),
        slug="deliverynote-list",
        description=_("Delivery notes management"),
        url=reverse("deliverynote_list"),
        menu=stock_menu
    )

    warehouse_dashboard_link, is_new = Link.objects.get_or_create(
        title=_("Details"),
        slug="warehouse-details",
        url="{% url warehouse_detail object.pk %}",
        menu=warehouse_menu
    )

    warehouse_movements_link, is_new = Link.objects.get_or_create(
        title=_("Movements"),
        slug="warehouse-movements",
        url="{% url warehouse_movements object.pk %}",
        menu=warehouse_menu
    )

    warehouse_timeline_link, is_new = Link.objects.get_or_create(
        title=_("Timeline"),
        slug="warehouse-timeline",
        url="{% url warehouse_timeline object.pk %}",
        menu=warehouse_menu
    )

    deliverynote_details_link, is_new = Link.objects.get_or_create(
        title=_("Details"),
        slug="deliverynote-details",
        url="{% url deliverynote_detail object.object_id %}",
        menu=deliverynote_menu
    )

    deliverynote_hard_copies_link, is_new = Link.objects.get_or_create(
        title=_("Hard copies"),
        slug="deliverynote-hardcopies",
        url="{% url deliverynote_hardcopies object.object_id %}",
        menu=deliverynote_menu
    )

    deliverynote_timeline_link, is_new = Link.objects.get_or_create(
        title=_("Timeline"),
        slug="deliverynote-timeline",
        url="{% url deliverynote_timeline object.object_id %}",
        menu=deliverynote_menu
    )
    
    # Signatures.
    warehouse_created_signature, is_new = Signature.objects.get_or_create(
        title=_("Warehouse created"),
        slug="warehouse-created"
    )

    warehouse_deleted_signature, is_new = Signature.objects.get_or_create(
        title=_("Warehouse deleted"),
        slug="warehouse-deleted"
    )

    movement_created_signature, is_new = Signature.objects.get_or_create(
        title=_("Movement created"),
        slug="movement-created"
    )

    movement_deleted_signature, is_new = Signature.objects.get_or_create(
        title=_("Movement deleted"),
        slug="movement-deleted"
    )

    deliverynote_created_signature, is_new = Signature.objects.get_or_create(
        title=_("Delivery note created"),
        slug="deliverynote-created"
    )

    deliverynote_changed_signature, is_new = Signature.objects.get_or_create(
        title=_("Delivery note changed"),
        slug="deliverynote-changed"
    )

    deliverynote_deleted_signature, is_new = Signature.objects.get_or_create(
        title=_("Delivery note deleted"),
        slug="deliverynote-deleted"
    )

    # Groups.
    purchase_team_group, is_new = Group.objects.get_or_create(
        name=_('Purchase Team')
    )

    purchase_managers_group, is_new = Group.objects.get_or_create(
        name=_('Purchase Managers')
    )

    # Permissions.
    can_view_warehouse, is_new = MyPermission.objects.get_or_create_by_natural_key("view_warehouse", "stock", "warehouse")
    can_add_warehouse, is_new = MyPermission.objects.get_or_create_by_natural_key("add_warehouse", "stock", "warehouse")
    can_change_warehouse, is_new = MyPermission.objects.get_or_create_by_natural_key("change_warehouse", "stock", "warehouse")
    can_delete_warehouse, is_new = MyPermission.objects.get_or_create_by_natural_key("delete_warehouse", "stock", "warehouse")
    can_view_movement, is_new = MyPermission.objects.get_or_create_by_natural_key("view_movement", "stock", "movement")
    can_add_movement, is_new = MyPermission.objects.get_or_create_by_natural_key("add_movement", "stock", "movement")
    can_change_movement, is_new = MyPermission.objects.get_or_create_by_natural_key("change_movement", "stock", "movement")
    can_delete_movement, is_new = MyPermission.objects.get_or_create_by_natural_key("delete_movement", "stock", "movement")
    can_view_deliverynote, is_new = MyPermission.objects.get_or_create_by_natural_key("view_deliverynote", "stock", "deliverynote")
    can_add_deliverynote, is_new = MyPermission.objects.get_or_create_by_natural_key("add_deliverynote", "stock", "deliverynote")
    can_change_deliverynote, is_new = MyPermission.objects.get_or_create_by_natural_key("change_deliverynote", "stock", "deliverynote")
    can_delete_deliverynote, is_new = MyPermission.objects.get_or_create_by_natural_key("delete_deliverynote", "stock", "deliverynote")

    stock_link.only_with_perms.add(can_view_deliverynote)
    warehouses_link.only_with_perms.add(can_view_warehouse)
    movements_link.only_with_perms.add(can_view_movement)
    deliverynotes_link.only_with_perms.add(can_view_deliverynote)

    administrative_employees_group.permissions.add(can_view_deliverynote, can_add_deliverynote)
    purchase_team_group.permissions.add(can_view_warehouse, can_add_warehouse, can_view_movement, can_add_movement, can_view_deliverynote, can_add_deliverynote)
    purchase_managers_group.permissions.add(can_view_warehouse, can_add_warehouse, can_change_warehouse, can_delete_warehouse, can_view_movement, can_add_movement, can_change_movement, can_delete_movement, can_view_deliverynote, can_add_deliverynote, can_change_deliverynote, can_delete_deliverynote)

post_migrate.connect(install, dispatch_uid="install_stock")
