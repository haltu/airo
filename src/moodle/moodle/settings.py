# -*- coding: utf-8 -*-
#
# Copyright Haltu Oy, info@haltu.fi
# Licensed under the EUPL v1.1
#

from django.conf import settings

API_KEY = getattr(settings, 'MOODLE_API_KEY', '')
ENDPOINT = getattr(settings, 'MOODLE_ENDPOINT', '')

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

