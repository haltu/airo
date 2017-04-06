# -*- coding: utf-8 -*-
#
# Copyright Haltu Oy, info@haltu.fi
# Licensed under the EUPL v1.1
#

from project.settings import *

# Override these in local_settings.py

SECRET_KEY = ''

SIMPLEVIDEOS_GOOGLE_API_KEY = ''

MOODLE_API_KEY = ''
MOODLE_ENDPOINT = ''

DREAMDIKAIOS_CLIENT_IDENTIFIER = ''
DREAMDIKAIOS_BACKEND_URL = ''
DREAMDIKAIOS_BACKEND_VIEW_URL = ''
DREAMDIKAIOS_SECRET_KEY = ''

WILMA_BASE_URL = ''

LOGOUT_URL = ''

AIRO_CITY_CODE = ''

# -----

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True

DEBUG = False

INSTALLED_APPS += (
  'djsupervisor',
  'south',
)

# Address celery problems (task #5540)
BROKER_HEARTBEAT = 0
CELERYD_HIJACK_ROOT_LOGGER = False

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

