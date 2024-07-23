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
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

from .core.auth.forms import UserEditForm

class UserRegistrationForm(UserEditForm):
    """Form for user registration.
    """
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['tos'] = forms.BooleanField(widget=forms.CheckboxInput(), label=mark_safe(_(u'I have read and agree to the <a href="/terms-service" target="_blank">Terms of Service</a>')), error_messages={ 'required': u"You must agree to the terms to register." })
        self.fields['pp'] = forms.BooleanField(widget=forms.CheckboxInput(), label=mark_safe(_(u'I have read and agree to the <a href="/privacy" target="_blank">Privacy Policy</a>')), error_messages={ 'required': u"You must agree to the privacy policy to register." })
        del self.fields['is_staff']
        del self.fields['is_active']
        del self.fields['is_superuser']
        del self.fields['groups']
        del self.fields['user_permissions']
    
    
