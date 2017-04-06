# -*- coding: utf-8 -*-
#
# Copyright Haltu Oy, info@haltu.fi
# Licensed under the EUPL v1.1
#

import logging
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from moodle.models import MoodleUser
from moodle.api import fetch_users

LOG = logging.getLogger(__name__)


class Command(BaseCommand):
  help = 'Populate Moodle IDs for users'

  def handle(self, *args, **options):
    self.stdout.write('Starting to pull users from moodle api\n')
    user_count = self.do_fetch()
    self.stdout.write('Successfully updated %d moodle user ids\n' % user_count)

  def _map_keys(self, d):
    try:
      out = {}
      out['username'] = d['username']
      out['first_name'] = d['firstname']
      out['last_name'] = d['lastname']
      out['email'] = d['email']
      out['id'] = d['id']
    except KeyError:
      LOG.warning('Could not parse moodle user', extra={'data': {'data': d}})
      return {}
    return out

  def update_user(self, u):
    LOG.info('Updating user %(username)s' % u, extra={'data': u})
    try:
      u_obj = User.objects.get(username=u['username'])
    except User.DoesNotExist:
      return 0
    if not hasattr(u_obj, 'moodle'):
      MoodleUser.objects.create(user=u_obj, moodle_id=u['id'])
      return 1
    else:
      if u_obj.moodle.moodle_id == u['id']:
        # ok
        return 0
      else:
        # uh oh, confused
        self.stdout.write('Username/ID mismatch! We have user %s with ID %s, Moodle has ID %s'%(u_obj.username, u_obj.moodle.moodle_id, u['id']))
        return 0
    return 0

  def do_fetch(self):
    users = fetch_users()
    count = 0
    for u in map(self._map_keys, users):
      if u:
        count += self.update_user(u)
    return count


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

