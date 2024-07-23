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

from django.utils.translation import gettext as _
from django.shortcuts import render_to_response, get_object_or_404
from django.urls import reverse
from django.views.generic.simple import redirect_to
from django.views.generic import list_detail, create_update
from django.template import RequestContext
from django.contrib import messages

from .core.auth.decorators import obj_permission_required as permission_required
from .core.views import filtered_list_detail
from prometeo.documents.models import *
from prometeo.documents.forms import *
from prometeo.documents.views import *
from prometeo.products.forms import ProductEntryFormset

from ..models import *
from ..forms import *

def _get_deliverynote(request, *args, **kwargs):
    note_id = kwargs.get('note_id', None)
    if note_id:
        return get_object_or_404(DeliveryNote, id=note_id)
    id = kwargs.get('id', None)
    if id:
        return get_object_or_404(DeliveryNote, id=id)
    return None

@permission_required('stock.view_deliverynote')
def deliverynote_list(request, page=0, paginate_by=10, **kwargs):
    """Shows a delivery note list.
    """
    return filtered_list_detail(
        request,
        Document.objects.get_for_content(DeliveryNote),
        fields=['code', 'author', 'created', 'owner'],
        page=page,
        paginate_by=paginate_by,
        template_name='stock/deliverynote_list.html',
        **kwargs
    )

@permission_required('stock.add_deliverynote')     
def deliverynote_add(request, **kwargs):
    """Adds a new delivery note.
    """
    deliverynote = DeliveryNote()
    doc = Document(author=request.user, content_object=deliverynote)
      
    if request.method == 'POST':
        dform = DocumentForm(request.POST, instance=doc)
        form = DeliveryNoteForm(request.POST, instance=deliverynote)
        formset = ProductEntryFormset(request.POST)
        if form.is_valid() and dform.is_valid() and formset.is_valid():
            form.save()
            doc.content_object = deliverynote 
            dform.save()
            for e in formset.save():
                deliverynote.entries.add(e)
            messages.success(request, _("The delivery note was created successfully."))
            return redirect_to(request, url=doc.get_absolute_url())
    else:
        dform = DocumentForm(instance=doc)
        form = DeliveryNoteForm(instance=deliverynote)
        formset = ProductEntryFormset()

    return render_to_response('stock/deliverynote_edit.html', RequestContext(request, {'form': form, 'dform': dform, 'formset': formset, 'object': doc}))

@permission_required('stock.view_deliverynote', _get_deliverynote)     
def deliverynote_detail(request, id, page=None, **kwargs):
    """Shows delivery note details.
    """
    object_list = Document.objects.get_for_content(DeliveryNote)

    return list_detail.object_detail(
        request,
        object_id=object_list.get(object_id=id).pk,
        queryset=object_list,
        extra_context={
            'object_list': object_list,
        },
        template_name=kwargs.pop('template_name', 'stock/deliverynote_detail.html'),
        **kwargs
    )

@permission_required('stock.change_deliverynote', _get_deliverynote)     
def deliverynote_edit(request, id, **kwargs):
    """Edits a delivery note.
    """
    doc = get_object_or_404(Document.objects.get_for_content(DeliveryNote), object_id=id)
    deliverynote = doc.content_object
      
    if request.method == 'POST':
        dform = DocumentForm(request.POST, instance=doc)
        form = DeliveryNoteForm(request.POST, instance=deliverynote)
        formset = ProductEntryFormset(request.POST, queryset=deliverynote.entries.all())
        if form.is_valid() and dform.is_valid() and formset.is_valid():
            form.save()
            dform.save()
            for e in formset.save():
                deliverynote.entries.add(e)
            messages.success(request, _("The delivery note was updated successfully."))
            return redirect_to(request, url=doc.get_absolute_url())
    else:
        dform = DocumentForm(instance=doc)
        form = DeliveryNoteForm(instance=deliverynote)
        formset = ProductEntryFormset(queryset=deliverynote.entries.all())

    return render_to_response('stock/deliverynote_edit.html', RequestContext(request, {'form': form, 'dform': dform, 'formset': formset, 'object': doc}))

@permission_required('stock.delete_deliverynote', _get_deliverynote)    
def deliverynote_delete(request, id, **kwargs):
    """Deletes a delivery note.
    """
    return create_update.delete_object(
        request,
        model=Document,
        object_id=Document.objects.get_for_content(DeliveryNote).get(object_id=id).pk,
        post_delete_redirect=reverse('deliverynote_list'),
        template_name='stock/deliverynote_delete.html',
        **kwargs
    )

@permission_required('stock.view_deliverynote', _get_deliverynote)     
def deliverynote_hardcopies(request, id, page=0, paginate_by=10, **kwargs):
    """Shows delivery note hard copies.
    """
    return hardcopy_list(request, Document.objects.get_for_content(DeliveryNote).get(object_id=id).pk, page, paginate_by, **kwargs)

@permission_required('stock.change_deliverynote', _get_deliverynote)     
def deliverynote_add_hardcopy(request, id, **kwargs):
    """Adds an hard copy to the given document.
    """
    return hardcopy_add(request, Document.objects.get_for_content(DeliveryNote).get(object_id=id).pk, **kwargs)
