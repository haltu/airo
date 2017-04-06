# -*- coding: utf-8 -*-
#
# Copyright Haltu Oy, info@haltu.fi
# Licensed under the EUPL v1.1
#

import logging
from django.dispatch import Signal


LOG = logging.getLogger(__name__)

# sender = User logging out
logout_initiated = Signal(providing_args=['request'])


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

