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

import re
from copy import copy

from django import template
from django.utils.translation import gettext_lazy as _

from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist
import json

from ..models import Widget

register = template.Library()

class WidgetNode(template.Node):
    def __init__(self, widget_slug, template=None):
        self.template = template
        try:
            self.widget = Widget.objects.get(slug=widget_slug)
            if self.template is None:
                self.template = self.widget.template
        except ObjectDoesNotExist:
            self.widget = None

    def render(self, context):
        output = ''
        context = copy(context)
        if self.widget:
            if self.widget.template.context:
                context.update(json.loads(self.widget.template.context))
            if self.widget.context:
                context.update(json.loads(self.widget.context))
            pkg, sep, name = self.widget.template.source.rpartition('.')
            try:
                m = __import__(pkg, {}, {}, [name])
                func = getattr(m, name)
                context = func(context)
            except:
                pass
            output += render_to_string(self.template.template_name, {'widget': self.widget}, context)
        return output
        
@register.tag
def widget(parser, token):
    widget_slug = ''
    template = None
    try:
        args = token.split_contents()
        if len(args) < 2:
            raise ValueError
        elif len(args) == 2:
            widget_slug = args[1].strip("'").strip('"')
        else:
            widget_slug = args[1].strip("'").strip('"')
            template = args[2].strip("'").strip('"')
    except ValueError:
        raise template.TemplateSyntaxError(
            f"{token.contents.split()[0]} tag requires a single argument"
        )

    return WidgetNode(widget_slug, template)
