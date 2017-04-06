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
  help = 'Fetch users from moodle and add them as User objects'

  def handle(self, *args, **options):
    self.stdout.write('Starting to pull users from moodle api\n')
    user_count = self.do_fetch()
    self.stdout.write('Successfully fetched %d moodle users\n' % user_count)

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

  def create_user(self, u):
    LOG.info('Adding user %(username)s' % u, extra={'data': u})
    try:
      u_obj = User.objects.get(moodle__moodle_id=u['id'])
    except User.DoesNotExist:
      if User.objects.filter(username=u['username']).exists():
        self.stdout.write('Error, duplicate username: %s'%u['username'])
        return None
      else:
        u_obj = User.objects.create(username=u['username'])
        MoodleUser.objects.create(user=u_obj, moodle_id=u['id'])
    u_obj.username = u['username']
    u_obj.first_name = u['first_name']
    u_obj.last_name = u['last_name']
    u_obj.email = u['email']
    u_obj.save()
    return u_obj

  def do_fetch(self):
    users = fetch_users()
    count = 0
    for u in map(self._map_keys, users):
      if u:
        self.create_user(u)
        count += 1
    return count

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

