# -*- coding: utf-8 -*-
#
# Copyright Haltu Oy, info@haltu.fi
# Licensed under the EUPL v1.1
#

import logging
import json
from django.core.management.base import BaseCommand
from moodle.api import fetch_users

LOG = logging.getLogger(__name__)


class Command(BaseCommand):
  help = 'Print user data from moodle'

  def handle(self, *args, **options):
    self.do_print()

  def do_print(self):
    users = fetch_users()
    self.stdout.write(json.dumps(users, indent=4))

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

