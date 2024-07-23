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

from django import forms
from django.utils.translation import gettext as _

from .core.forms import enrich_form
from .core.forms.widgets import *
from prometeo.partners.models import Partner

from .models import *

class WarehouseForm(forms.ModelForm):
    """Form for warehouse data.
    """
    class Meta:
        model = Warehouse
        exclude = ['author', 'stream', 'dashboard']
        widgets = {
            'owner': SelectAndAddWidget(add_url='/partners/add', with_perms=['partners.add_partner']),
            'address': SelectAndAddWidget(add_url='/addresses/add', with_perms=['addressing.add_address'])
        }
        
class MovementForm(forms.ModelForm):
    """Form for movement data.
    """
    class Meta:
        model = Movement
        exclude = ['product_entry', 'author']
        widgets = {
            'origin': SelectAndAddWidget(add_url='/warehouses/add', with_perms=['stock.add_warehouse']),
            'destination': SelectAndAddWidget(add_url='/warehouses/add', with_perms=['stock.add_warehouse'])
        }

    def clean_destination(self):
        destination = self.cleaned_data['destination']

        if destination == (self.cleaned_data.get('origin', None) or self.instance.origin):
            raise forms.ValidationError(_("Origin and destination warehouses can't be the same."))

        return destination
        
class IngoingMovementForm(MovementForm):
    """Form for ingoing movement data.
    """
    class Meta(MovementForm.Meta):
        exclude = ['product_entry', 'destination', 'author']

    def __init__(self, *args, **kwargs):
        super(IngoingMovementForm, self).__init__(*args, **kwargs)
        self.fields['origin'].queryset = Warehouse.objects.exclude(pk=self.instance.destination.pk)

    def clean_origin(self):
        origin = self.cleaned_data['origin']

        if origin == (self.cleaned_data.get('destination', None) or self.instance.destination):
            raise forms.ValidationError(_("Origin and destination warehouses can't be the same."))

        return origin
        
class OutgoingMovementForm(MovementForm):
    """Form for outgoing movement data.
    """
    class Meta(MovementForm.Meta):
        exclude = ['product_entry', 'origin', 'author']

    def __init__(self, *args, **kwargs):
        super(OutgoingMovementForm, self).__init__(*args, **kwargs)
        self.fields['destination'].queryset = Warehouse.objects.exclude(pk=self.instance.origin.pk)

class DeliveryNoteForm(forms.ModelForm):
    """Form for delivery note data.
    """
    class Meta:
        model = DeliveryNote
        exclude = ['document', 'entries']
        widgets = {
            'invoice_addressee': SelectAndAddWidget(add_url='/partners/add', with_perms=['partners.add_partner']),
            'delivery_addressee': SelectAndAddWidget(add_url='/partners/add', with_perms=['partners.add_partner']),
            'order_ref_date': DateWidget(),
            'delivery_date': DateWidget()
        }

enrich_form(WarehouseForm)
enrich_form(MovementForm)
enrich_form(DeliveryNoteForm)
