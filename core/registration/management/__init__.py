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

from core.utils import check_dependency
from core.widgets.models import *
from core.menus.models import *

check_dependency('.core.menus')
check_dependency('.core.auth')

def install(sender, **kwargs):
    user_area_not_logged_menu, is_new = Menu.objects.get_or_create(slug="user_area_not_logged")
    
    # Links.
    register_link, is_new = Link.objects.get_or_create(
        title=_("Register"),
        slug="register",
        description=_("Register a new account"),
        url=reverse("user_register"),
        only_authenticated=False,
        menu=user_area_not_logged_menu
    )

post_migrate.connect(install, dispatch_uid="install_notifications")
