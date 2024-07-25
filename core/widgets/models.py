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

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.utils.views  import validate_json
from django.urls import reverse
    
class Region(models.Model):
    """Region model.
    """
    slug = models.SlugField(max_length=100, unique=True, verbose_name=_('slug'))
    description = models.TextField(blank=True, null=True, verbose_name=_('description'))

    class Meta:
        verbose_name = _('region')
        verbose_name_plural = _('regions')

    def __unicode__(self):
        return self.slug

class WidgetTemplate(models.Model):
    """WidgetTemplate model.
    """
    title = models.CharField(max_length=100, verbose_name=_('title'))
    slug = models.SlugField(unique=True, verbose_name=_('slug'))
    description = models.TextField(blank=True, null=True, verbose_name=_('description'))
    source = models.CharField(blank=False, null=False, max_length=200, verbose_name=_('source'))
    template_name = models.CharField(blank=True, null=True, max_length=200, default="widgets/widget.html", verbose_name=_('template name'))
    context = models.TextField(blank=True, null=True, validators=[validate_json], help_text=_('Use the JSON syntax.'), verbose_name=_('context'))
    public = models.BooleanField(default=True, verbose_name=_('public?'))
    
    class Meta:
        ordering = ('title',)
        verbose_name = _('widget template')
        verbose_name_plural = _('widget templates')

    def __unicode__(self):
        return u"%s" % self.title

class Widget(models.Model):
    """Widget model.
    """
    title = models.CharField(max_length=100, verbose_name=_('title'))
    slug = models.SlugField(unique=True, verbose_name=_('slug'))
    region = models.ForeignKey(Region, related_name='widgets', 
                               verbose_name=_('region'), on_delete=models.CASCADE)
    template = models.ForeignKey(WidgetTemplate, related_name='instances', verbose_name=_('template'), on_delete=models.CASCADE)
    context = models.TextField(blank=True, null=True, validators=[validate_json], 
                help_text=_('Use the JSON syntax.'), verbose_name=_('context'), )
    show_title = models.BooleanField(default=True, verbose_name=_('show title'))
    editable = models.BooleanField(default=False, verbose_name=_('editable'))
    sort_order = models.PositiveIntegerField(default=0, verbose_name=_('sort order'))

    class Meta:
        ordering = ('region', 'sort_order', 'title',)
        verbose_name = _('widget')
        verbose_name_plural = _('widgets')

    def __unicode__(self):
        return u"%s | %s" % (self.region, self.title)

    def get_edit_url(self):
        def get_absolute_url(self):
            return reverse('widget_edit', (), args={"slug": self.slug})

    def get_delete_url(self):
        return reverse('widget_delete', (), {"slug": self.slug})
