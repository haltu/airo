# -*- coding: utf-8 -*-
#
# Copyright Haltu Oy, info@haltu.fi
# Licensed under the EUPL v1.1
#

import logging
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render
from django.utils.http import is_safe_url
from airo.signals import logout_initiated
from airo import settings


LOG = logging.getLogger(__name__)

def logout_view(request):
  logout_initiated.send_robust(sender=request.user, request=request)
  result = logout(request)
  if not settings.LOGOUT_URL:
    return result
  return redirect(settings.LOGOUT_URL)


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

