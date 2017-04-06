# -*- coding: utf-8 -*-
#
# Copyright Haltu Oy, info@haltu.fi
# Licensed under the EUPL v1.1
#

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

# Filter available permission which are displayed in useradmin for Card
# syntax: iterable containing tuples of ('app_label', 'model', 'codename')
# example: (('airo', 'airo', 'supervisor'), ('airo', 'airo', 'user'))
USERADMIN_CARD_PERMISSION_FILTER = getattr(settings, 'AIRO_USERADMIN_PERMISSION_FILTER', [])

LOGOUT_URL = getattr(settings, 'LOGOUT_URL', '')

CITY_CODE = getattr(settings, 'AIRO_CITY_CODE', None)

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

