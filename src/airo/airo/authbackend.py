# -*- coding: utf-8 -*-
#
# Copyright Haltu Oy, info@haltu.fi
# Licensed under the EUPL v1.1
#

import logging
from dreamsso.models import User
#from django.contrib.auth.models import User
from shibboleth.authbackend import ShibbolethBackend

LOG = logging.getLogger(__name__)


class AiroShibbolethBackend(ShibbolethBackend):

  def authenticate(self, **credentials):
    username = self.clean_username(credentials)
    if username:
      try:
        user = User.objects.get(username=username)
        return user
      except User.DoesNotExist:
        pass

  def get_user(self, user_id):
    try:
      return User.objects.get(pk=user_id)
    except User.DoesNotExist:
      return None

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

