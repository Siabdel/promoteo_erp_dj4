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

check_dependency('.core.auth')

def install(sender, **kwargs):
    users_group, is_new = Group.objects.get_or_create(
        name=_('Users')
    )

    employees_group, is_new = Group.objects.get_or_create(
        name=_('Employees')
    )

    # Groups.
    administrative_employees_group, is_new = Group.objects.get_or_create(
        name=_('Administrative Employees')
    )

    # Permissions.
    can_view_address, is_new = MyPermission.objects.get_or_create_by_natural_key("view_address", "addressing", "address")
    can_add_address, is_new = MyPermission.objects.get_or_create_by_natural_key("add_address", "addressing", "address")
    can_change_address, is_new = MyPermission.objects.get_or_create_by_natural_key("change_address", "addressing", "address")
    can_delete_address, is_new = MyPermission.objects.get_or_create_by_natural_key("delete_address", "addressing", "address")

    can_view_phonenumber, is_new = MyPermission.objects.get_or_create_by_natural_key("view_phonenumber", "addressing", "phonenumber")
    can_add_phonenumber, is_new = MyPermission.objects.get_or_create_by_natural_key("add_phonenumber", "addressing", "phonenumber")
    can_change_phonenumber, is_new = MyPermission.objects.get_or_create_by_natural_key("change_phonenumber", "addressing", "phonenumber")
    can_delete_phonenumber, is_new = MyPermission.objects.get_or_create_by_natural_key("delete_phonenumber", "addressing", "phonenumber")

    can_view_socialprofile, is_new = MyPermission.objects.get_or_create_by_natural_key("view_socialprofile", "addressing", "socialprofile")
    can_add_socialprofile, is_new = MyPermission.objects.get_or_create_by_natural_key("add_socialprofile", "addressing", "socialprofile")
    can_change_socialprofile, is_new = MyPermission.objects.get_or_create_by_natural_key("change_socialprofile", "addressing", "socialprofile")
    can_delete_socialprofile, is_new = MyPermission.objects.get_or_create_by_natural_key("delete_socialprofile", "addressing", "socialprofile")

    users_group.permissions.add(can_view_address, can_view_phonenumber, can_view_socialprofile)

    employees_group.permissions.add(can_view_address, can_view_phonenumber, can_view_socialprofile)

    administrative_employees_group.permissions.add(can_add_address, can_change_address, can_delete_address)
    administrative_employees_group.permissions.add(can_add_phonenumber, can_change_phonenumber, can_delete_phonenumber)
    administrative_employees_group.permissions.add(can_add_socialprofile, can_change_socialprofile, can_delete_socialprofile)

post_migrate.connect(install, dispatch_uid="install_addressing")
