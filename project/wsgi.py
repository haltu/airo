# -*- coding: utf-8 -*-
#
# Copyright Haltu Oy, info@haltu.fi
# Licensed under the EUPL v1.1
#

from raven.contrib.django.raven_compat.middleware.wsgi import Sentry
from django.core.wsgi import get_wsgi_application

application = Sentry(get_wsgi_application())

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

