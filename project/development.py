# -*- coding: utf-8 -*-
#
# Copyright Haltu Oy, info@haltu.fi
# Licensed under the EUPL v1.1
#

from project.settings import *

# Override these in local_settings.py

SIMPLEVIDEOS_GOOGLE_API_KEY = ''

SAUCELABS_USERNAME = ''
SAUCELABS_ACCESS_KEY = ''

DREAMDIKAIOS_CLIENT_IDENTIFIER = ''
DREAMDIKAIOS_BACKEND_URL = ''
DREAMDIKAIOS_BACKEND_VIEW_URL = ''
DREAMDIKAIOS_SECRET_KEY = ''

# -----

DEBUG=True
TEMPLATE_DEBUG=DEBUG

COMPRESS_REBUILD_TIMEOUT = 1

INTERNAL_IPS = ('127.0.0.1',)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

MIDDLEWARE_CLASSES += (
  #'debug_toolbar.middleware.DebugToolbarMiddleware',
)

DEBUG_TOOLBAR_CONFIG = {
  'INTERCEPT_REDIRECTS': False,
}

LOGOUT_URL = '/'

INSTALLED_APPS += (
  #'debug_toolbar',
  'django_nose',
  'djsupervisor',
  'south',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'normal': {
            'format': '%(levelname)s %(name)s %(lineno)s %(message)s %(data)s'
        },
    },
    'filters': {
      'default': {
        '()': 'project.logging_helpers.Filter',
      },
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'normal',
            'filters': ['default'],
        },
    },
    'loggers': {
        'django': {
            'handlers':['null'],
            'propagate': True,
        },
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
        }
    }
}

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

