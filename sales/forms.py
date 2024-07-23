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

class BankAccountForm(forms.ModelForm):
    """Form for bank account data.
    """
    class Meta:
        model = BankAccount
        widgets = {
            'owner': SelectAndAddWidget(add_url='/partners/add', with_perms=['partners.add_partner']),
        }
        
class SalesInvoiceForm(forms.ModelForm):
    """Form for sales invoice data.
    """
    class Meta:
        model = SalesInvoice
        exclude = ['document', 'entries']
        widgets = {
            'invoice_addressee': SelectAndAddWidget(add_url='/partners/add', with_perms=['partners.add_partner']),
            'shipping_addressee': SelectAndAddWidget(add_url='/partners/add', with_perms=['partners.add_partner']),
            'order_ref_date': DateWidget(),
            'due_date': DateWidget(),
            'bank_account': SelectAndAddWidget(add_url='/bankaccounts/add', with_perms=['sales.add_bankaccount'])
        }

    def clean_terms_of_payment(self):
        owner = Partner.objects.get(id=self.data.get('owner', None))
        terms = self.cleaned_data['terms_of_payment']
        if not terms and owner:
            terms = owner.terms_of_payment
        return terms

enrich_form(BankAccountForm)
enrich_form(SalesInvoiceForm)
