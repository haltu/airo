# -*- coding: utf-8 -*-
#
# Copyright Haltu Oy, info@haltu.fi
# Licensed under the EUPL v1.1
#

from django.utils.translation import ugettext as _
from django.db import models


class Airo(models.Model):
  class Meta:
    permissions = (
      ('supervisor', 'User is supervisor'),
      ('user', 'User is basic user'),
    )


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

