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

from django.utils.translation import gettext_lazy as _

LEAD_STATUS_CHOICES = (
    ('FIRST', _('first contact')),
    ('HOT', _('hot contact')),
    ('COLD', _('cold contact')),
)

LEAD_DEFAULT_STATUS = 'FIRST'

CURRENCIES = (
    ('AED', _('AED')),
    ('AFN', _('AFN')),
    ('ALL', _('ALL')),
    ('AMD', _('AMD')),
    ('ANG', _('ANG')),
    ('AOA', _('AOA')),
    ('ARS', _('ARS')),
    ('AUD', _('AUD')),
    ('AZN', _('AZN')),
    ('BAM', _('BAM')),
    ('BBD', _('BBD')),
    ('BDT', _('BDT')),
    ('BGN', _('BGN')),
    ('BHD', _('BHD')),
    ('BIF', _('BIF')),
    ('BMD', _('BMD')),
    ('BND', _('BND')),
    ('BOB', _('BOB')),
    ('BRL', _('BRL')),
    ('BSD', _('BSD')),
    ('BTN', _('BTN')),
    ('BWP', _('BWP')),
    ('BYR', _('BYR')),
    ('BZD', _('BZD')),
    ('CAD', _('CAD')),
    ('CDF', _('CDF')),
    ('CFA', _('CFA')),
    ('CFP', _('CFP')),
    ('CHF', _('CHF')),
    ('CLP', _('CLP')),
    ('CNY', _('CNY')),
    ('COP', _('COP')),
    ('CRC', _('CRC')),
    ('CUC', _('CUC')),
    ('CZK', _('CZK')),
    ('DJF', _('DJF')),
    ('DKK', _('DKK')),
    ('DOP', _('DOP')),
    ('DZD', _('DZD')),
    ('EEK', _('EEK')),
    ('EGP', _('EGP')),
    ('ERN', _('ERN')),
    ('ETB', _('ETB')),
    ('EUR', _('EUR')),
    ('FJD', _('FJD')),
    ('FKP', _('FKP')),
    ('FMG', _('FMG')),
    ('GBP', _('GBP')),
    ('GEL', _('GEL')),
    ('GHS', _('GHS')),
    ('GIP', _('GIP')),
    ('GMD', _('GMD')),
    ('GNF', _('GNF')),
    ('GQE', _('GQE')),
    ('GTQ', _('GTQ')),
    ('GYD', _('GYD')),
    ('HKD', _('HKD')),
    ('HNL', _('HNL')),
    ('HRK', _('HRK')),
    ('HTG', _('HTG')),
    ('HUF', _('HUF')),
    ('IDR', _('IDR')),
    ('ILS', _('ILS')),
    ('INR', _('INR')),
    ('IQD', _('IQD')),
    ('IRR', _('IRR')),
    ('ISK', _('ISK')),
    ('JMD', _('JMD')),
    ('JOD', _('JOD')),
    ('JPY', _('JPY')),
    ('KES', _('KES')),
    ('KGS', _('KGS')),
    ('KHR', _('KHR')),
    ('KMF', _('KMF')),
    ('KPW', _('KPW')),
    ('KRW', _('KRW')),
    ('KWD', _('KWD')),
    ('KYD', _('KYD')),
    ('KZT', _('KZT')),
    ('LAK', _('LAK')),
    ('LBP', _('LBP')),
    ('LKR', _('LKR')),
    ('LRD', _('LRD')),
    ('LSL', _('LSL')),
    ('LTL', _('LTL')),
    ('LVL', _('LVL')),
    ('LYD', _('LYD')),
    ('MAD', _('MAD')),
    ('MDL', _('MDL')),
    ('MGA', _('MGA')),
    ('MKD', _('MKD')),
    ('MMK', _('MMK')),
    ('MNT', _('MNT')),
    ('MOP', _('MOP')),
    ('MRO', _('MRO')),
    ('MUR', _('MUR')),
    ('MVR', _('MVR')),
    ('MWK', _('MWK')),
    ('MXN', _('MXN')),
    ('MYR', _('MYR')),
    ('MZM', _('MZM')),
    ('NAD', _('NAD')),
    ('NGN', _('NGN')),
    ('NIO', _('NIO')),
    ('NOK', _('NOK')),
    ('NPR', _('NPR')),
    ('NRs', _('NRs')),
    ('NZD', _('NZD')),
    ('OMR', _('OMR')),
    ('PAB', _('PAB')),
    ('PEN', _('PEN')),
    ('PGK', _('PGK')),
    ('PHP', _('PHP')),
    ('PKR', _('PKR')),
    ('PLN', _('PLN')),
    ('PYG', _('PYG')),
    ('QAR', _('QAR')),
    ('RMB', _('RMB')),
    ('RON', _('RON')),
    ('RSD', _('RSD')),
    ('RUB', _('RUB')),
    ('RWF', _('RWF')),
    ('SAR', _('SAR')),
    ('SCR', _('SCR')),
    ('SDG', _('SDG')),
    ('SDR', _('SDR')),
    ('SEK', _('SEK')),
    ('SGD', _('SGD')),
    ('SHP', _('SHP')),
    ('SOS', _('SOS')),
    ('SRD', _('SRD')),
    ('STD', _('STD')),
    ('SYP', _('SYP')),
    ('SZL', _('SZL')),
    ('THB', _('THB')),
    ('TJS', _('TJS')),
    ('TMT', _('TMT')),
    ('TND', _('TND')),
    ('TRY', _('TRY')),
    ('TTD', _('TTD')),
    ('TWD', _('TWD')),
    ('TZS', _('TZS')),
    ('UAE', _('UAE')),
    ('UAH', _('UAH')),
    ('UGX', _('UGX')),
    ('USD', _('USD')),
    ('UYU', _('UYU')),
    ('UZS', _('UZS')),
    ('VEB', _('VEB')),
    ('VND', _('VND')),
    ('VUV', _('VUV')),
    ('WST', _('WST')),
    ('XAF', _('XAF')),
    ('XCD', _('XCD')),
    ('XDR', _('XDR')),
    ('XOF', _('XOF')),
    ('XPF', _('XPF')),
    ('YEN', _('YEN')),
    ('YER', _('YER')),
    ('YTL', _('YTL')),
    ('ZAR', _('ZAR')),
    ('ZMK', _('ZMK')),
    ('ZWR', _('ZWR')),
)

DEFAULT_CURRENCY = 'EUR'

TERMS_OF_PAYMENT = (
    ('30', _('30 days')),
    ('60', _('60 days')),
    ('90', _('90 days')),
    ('120', _('120 days')),
    ('CIA', _('cash in advance')),
    ('COD', _('cash on delivery')),
)

DEFAULT_TERMS_OF_PAYMENT = '30'

ROLES = (
    ('CHAIRMAN', _("Chairman")),
    ('CEO', _("CEO")),
    ('COO', _("COO")),
    ('CFO', _("CFO")),
    ('CTO', _("CTO")),
    ('PROJMANAGER', _("Project Manager")),
    ('SALESMANAGER', _("Sales Manager")),
    ('SALESMAN', _("Salesman")),
    ('EMPLOYEE', _("Employee")),
)

DEFAULT_ROLE = 'EMPLOYEE'

GENDERS = (
    ('M', _("Male")),
    ('F', _("Female")),
)
