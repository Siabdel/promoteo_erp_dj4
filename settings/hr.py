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

import datetime

from django.utils.translation import gettext as _

EMPLOYMENT_TYPE_CHOICES = (
    ('FT', _('fixed-term')),
    ('PT', _('part-time')),
    ('OE', _('open-ended')),
)

WORKING_DAY_START = datetime.time(9, 0)
WORKING_DAY_END = datetime.time(18, 30)

LAUNCH_TIME_START = datetime.time(13, 0)
LAUNCH_TIME_END = datetime.time(14, 30)

EXPENSE_TYPE_CHOICES = (
    ('TRV', _('travel')),
    ('MDC', _('medical')),
    ('FOD', _('food')),
    ('CAL', _('call')),
    ('OTH', _('others')),
)

DEFAULT_EXPENSE_TYPE = 'TRV'

LEAVE_TYPE_CHOICES = (
    ('CSL', _('casual')),
    ('MDC', _('medical')),
    ('SCK', _('sick')),
)

DEFAULT_LEAVE_TYPE = 'CSL'
