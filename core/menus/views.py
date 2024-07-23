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
from django.urls import reverse
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.contrib import messages

from core.utils import clean_referer
from .core.auth.views import _get_user
from .core.auth.decorators import obj_permission_required as permission_required
from .core.views import filtered_list_detail

from .models import *
from .forms import *

def _get_bookmark(request, *args, **kwargs):
    username = kwargs.get('username', None)
    slug = kwargs.get('slug', None)
    return get_object_or_404(Bookmark, menu__userprofile__user__username=username, slug=slug)

@permission_required('auth.view_user', _get_user)
@permission_required('menus.view_link')
def bookmark_list(request, username, page=0, paginate_by=10, **kwargs):
    """Displays the list of all bookmarks for the current user.
    """
    user = get_object_or_404(User, username=username)

    return filtered_list_detail(
        request,
        Bookmark.objects.filter(menu=user.get_profile().bookmarks),
        fields=['title', 'url', 'description', 'new_window'],
        paginate_by=paginate_by,
        page=page,
        extra_context={
            'object': user,
        },
        template_name='menus/bookmark_list.html',
        **kwargs
    )

@permission_required('auth.change_user', _get_user)
@permission_required('menus.add_link')
def bookmark_add(request, username, **kwargs):
    """Adds a new bookmark for the current user.
    """
    user = get_object_or_404(User, username=username)

    bookmarks = user.get_profile().bookmarks
    bookmark = Bookmark(menu=bookmarks, sort_order=bookmarks.links.count())

    if request.method == 'POST':
        form = BookmarkForm(request.POST, instance=bookmark)
        if form.is_valid():
            bookmark.slug = slugify("%s_%s" % (bookmark.title, user.pk))
            bookmark = form.save()
            messages.success(request, _("The bookmark was created successfully."))
            return redirect_to(request, url=reverse('bookmark_list', args=[user.username]))
    else:
        url = clean_referer(request)
        if url == reverse('bookmark_list', args=[user.username]):
            url = ""
        bookmark.url = url
        form = BookmarkForm(instance=bookmark)

    return render_to_response('menus/bookmark_edit.html', RequestContext(request, {'form': form, 'object': bookmark, 'object_user': user}))

@permission_required('auth.change_user', _get_user)
@permission_required('menus.change_link', _get_bookmark)
def bookmark_edit(request, username, slug, **kwargs):
    """Edits an existing bookmark for the current user.
    """
    user = get_object_or_404(User, username=username)

    bookmarks = user.get_profile().bookmarks
    bookmark = get_object_or_404(Bookmark, menu=bookmarks, slug=slug)

    if request.method == 'POST':
        form = BookmarkForm(request.POST, instance=bookmark)
        if form.is_valid():
            bookmark = form.save()
            messages.success(request, _("The bookmark was updated successfully."))
            return redirect_to(request, url=reverse('bookmark_list', args=[user.username]))
    else:
        form = BookmarkForm(instance=bookmark)

    return render_to_response('menus/bookmark_edit.html', RequestContext(request, {'form': form, 'object': bookmark, 'object_user': user}))

@permission_required('auth.change_user', _get_user)
@permission_required('menus.delete_link', _get_bookmark)
def bookmark_delete(request, username, slug, **kwargs):
    """Deletes an existing bookmark for the current user.
    """
    user = get_object_or_404(User, username=username)

    bookmarks = user.get_profile().bookmarks
    bookmark = get_object_or_404(Bookmark, menu=bookmarks, slug=slug)

    return create_update.delete_object(
        request,
        model=Bookmark,
        slug=slug,
        post_delete_redirect=reverse('bookmark_list', args=[user.username]),
        template_name='menus/bookmark_delete.html',
        extra_context={'object_user': user},
        **kwargs
     )
