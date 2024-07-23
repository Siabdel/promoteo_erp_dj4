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

import os

from django import template
from django.template.defaultfilters import filesizeformat
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.translation import gettext as _

from django.conf import settings

from core.utils import value_to_string
from core.filebrowser.models import FileInfo

register = template.Library()

def sort_files(files, order_by):
    if order_by:
        field = order_by
        verse = (order_by[0] == '-')
        if verse:
            field = order_by[1:]
        if field == 'size': 
            files.sort(key=FileInfo._get_size, reverse=verse)
        elif field == 'name':
            files.sort(key=FileInfo._get_name, reverse=verse)
        elif field == 'created':
            files.sort(key=FileInfo._get_created, reverse=verse)
        elif field == 'modified':
            files.sort(key=FileInfo._get_modified, reverse=verse)
    else:
        files.sort()
    return files

def header_template(field, css, order_by, url, label):
    output = '\t\t<th>'
    if css:
        output = '\t\t<th class="%s">' % css
    if order_by and field in order_by:
        verse = "-"
        aclass = "asc"
        if "-%s" % field in order_by:
            verse = ""
            aclass = "desc"
        output += '<a title="%s" class="%s" href="%sorder_by=%s%s">%s</a>' % (label, aclass, url, verse, field, label)
    else:
        output += '<a title="%s" href="%sorder_by=%s">%s</a>' % (label, url, field, label)
    output += '</th>\n'
    return output

def action_template(css, label, url_prefix, url):
    return '<span class="%s"><a title="%s" href="%s%s">%s</a></span>' % (css, label, url_prefix, url, label)

def actions_template(f, url_prefix):
    actions = []
    actions.append(action_template('move', _('Move'), url_prefix, reverse('file_move', args=[f.url[1:]])))
    actions.append(action_template('copy', _('Copy'), url_prefix, reverse('file_copy', args=[f.url[1:]])))
    actions.append(action_template('add_link', _('Make link'), url_prefix, reverse('file_mkln', args=[f.url[1:]])))
    actions.append(action_template('edit', _('Rename'), url_prefix, reverse('file_rename', args=[f.url[1:]])))
    actions.append(action_template('delete', _('Delete'), url_prefix, reverse('file_delete', args=[f.url[1:]])))
    return '<span class="actions">%s</span>' % ' '.join(actions)

def row_template(index, path, f, url_prefix):
    output = []
    row_class = 'altrow' if index % 2 == 1 else ''
    
    if f == path.parent:
        output.append(format_html(
            '<tr class="{}">'
            '<td><a class="backlink" title="{}" href="{}{}">{}</a></td>'
            '<td class="number"></td><td></td><td></td><td></td>'
            '</tr>',
            row_class, f.name, url_prefix, f.url, _('Parent folder')
        ))
    else:
        file_type = ''
        if f.is_folder():
            file_type = format_html('<span class="folder">[{}]</span> ', _('Folder'))
        elif f.ext:
            file_type = format_html('<span class="file ext-{}">[{}]</span> ', f.ext.lower(), _('File'))
        else:
            file_type = format_html('<span class="file">[{}]</span> ', _('File'))

        name_link = ''
        if f.is_broken_link():
            name_link = format_html('{} <span class="broken_link">[{}]</span>', f.name, _('Broken link'))
        else:
            name_link = format_html('<a title="{}" href="{}{}">{}</a>', f.name, url_prefix, f.url, f.name)
            if f.is_link():
                name_link += format_html(' <span class="link">[{}]</span>', _('Link'))

        actions = actions_template(f, url_prefix)

        output.append(format_html(
            '<tr class="{}">'
            '<td>{}{}</td>'
            '<td class="number">{}</td>'
            '<td>{}</td>'
            '<td>{}</td>'
            '<td>{}</td>'
            '</tr>',
            row_class, file_type, name_link, filesizeformat(f.size),
            value_to_string(f.created), value_to_string(f.modified), mark_safe(actions)
        ))

    return ''.join(output)

@register.simple_tag(takes_context=True)
def filebrowser_actions(context, path=settings.MEDIA_ROOT, url_prefix=""):
    """Renders default file browser actions.
    """
    fi = FileInfo(path or settings.MEDIA_ROOT)
    output = '<ul>\n'
    output += '\t<li class="add"><a title="%(label)s" href="%(url_prefix)s%(url)s">%(label)s</a></li>\n' % {
        'label': _('Add folder'),
        'url_prefix': url_prefix,
        'url': reverse('file_mkdir', args=[fi.url[1:]])
    }
    output += '\t<li class="import"><a title="%(label)s" href="%(url_prefix)s%(url)s">%(label)s</a></li>\n' % {
        'label': _('Upload file'),
        'url_prefix': url_prefix,
        'url': reverse('file_upload', args=[fi.url[1:]])
    }
    output += '\t<li class="refresh"><a title="%(label)s" href="%(url)s">%(label)s</a></li>\n' % {'label': _('Refresh'), 'url': context['request'].path}
    output += '</ul>\n'
    return output    

@register.simple_tag(takes_context=True)
def filebrowser(context, path=settings.MEDIA_ROOT, root_path=settings.MEDIA_ROOT, url_prefix=""):
    """Renders a file browser.
    """
    request = context['request']
    url = '%s/?' % request.path.rstrip('/') + ''.join(['%s=%s&' % (key, value) for key, value in request.GET.items() if key != "order_by"])
    order_by = request.GET.get('order_by', None)
    fi = FileInfo(path or settings.MEDIA_ROOT)
    root = FileInfo(root_path or settings.MEDIA_ROOT)
    if fi.is_folder():
        files = [FileInfo(os.path.join(fi.path, f)) for f in os.listdir(fi.abspath)]
        files = sort_files(files, order_by)
        if fi.parent and fi.abspath != root:
            files = [fi.parent] + files
        output = '<table class="filebrowser">\n'
        output += '\t<tr>\n'
        output += header_template('name', 'char', order_by, url, _('Name'))
        output += header_template('size', 'size', order_by, url, _('Size'))
        output += header_template('created', None, order_by, url, _('Created'))
        output += header_template('modified', None, order_by, url, _('Modified'))
        output += '\t\t<th class="actions"></th>\n'
        output += '\t</tr>\n'
        for i, f in enumerate(files):
            output += row_template(i, fi, f, url_prefix)
        output += '</table>\n'
        output += '<div class="folder_meta"><p><strong>%d</strong> %s, %s</p></div>' % (len(files), _('element(s)'), filesizeformat(fi.size))
        return output
    return ''
