# -*- coding: utf-8 -*-
#
# Copyright Haltu Oy, info@haltu.fi
# Licensed under the EUPL v1.1
#

from django.conf import settings

BASE_URL = getattr(settings, 'WILMA_BASE_URL', '')
SESSION_COOKIE_NAME = settings.SESSION_COOKIE_NAME

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

