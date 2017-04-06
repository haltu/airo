# -*- coding: utf-8 -*-
#
# Copyright Haltu Oy, info@haltu.fi
# Licensed under the EUPL v1.1
#

from django.db import models
from django.contrib.auth.models import User


class MoodleUser(models.Model):
  user = models.OneToOneField(User, related_name='moodle')
  moodle_id = models.IntegerField(blank=True, null=True)


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

