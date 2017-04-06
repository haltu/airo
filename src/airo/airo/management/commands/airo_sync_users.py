# -*- coding: utf-8 -*-
#
# Copyright Haltu Oy, info@haltu.fi
# Licensed under the EUPL v1.1
#

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import logging
from moodle.management.commands import fetch_moodle_users
from wilma.models import WilmaUser, WilmaSettings
from dreamdikaios.dreamdikaiosusers.models import DikaiosProfile
from dreamsso.models import User
from dreamuserdb.models import Organisation, Role, User as UserdbUser
from dreamcards.models import UserGroup
from airo import settings

LOG = logging.getLogger(__name__)


class Command(fetch_moodle_users.Command):
  def __init__(self, *args, **kwargs):
    super(Command, self).__init__(*args, **kwargs)
    self.city_code = settings.CITY_CODE

  def handle(self, *args, **kwargs):
    self.organisation, c = Organisation.objects.get_or_create(source='hameenlinna', name='hameenlinna', defaults={'title': u'Hämeenlinna'})
    self.roles = {}
    self.roles['student'], _ = Role.objects.get_or_create(name='students', title='students', official=True, organisation=self.organisation)
    self.roles['teacher'], _ = Role.objects.get_or_create(name='teachers', title='teachers', official=True, organisation=self.organisation)
    self.roles['staff'], _ = Role.objects.get_or_create(name='staff', title='staff', official=True, organisation=self.organisation)
    super(Command, self).handle(*args, **kwargs)

  def _map_keys(self, d):
    out = super(Command, self)._map_keys(d)
    extra = {}
    if 'institution' in d:
      extra['role'] = d['institution']
    if 'address' in d:
      extra['personal_identity_code_hash'] = d['address']
    if 'description' in d:
      extra['description'] = d['description']
    if 'city' in d:
      extra['school'] = d['city']
    if 'department' in d:
      extra['school_code'] = d['department']
    out.update(extra)
    return out

  def create_user(self, u):
    u_obj = super(Command, self).create_user(u)
    if u_obj is not None:
      dream_user = User.objects.get(pk=u_obj.pk)
      self.create_wilma_profile(dream_user, u)
      self.create_usergroups(dream_user, u)
      self.assign_organisation(dream_user, u)
      self.assign_role(dream_user, u)
      self.create_dikaios_profile(dream_user, u)
      self.refresh_permissions(dream_user)
    return u_obj

  def assign_organisation(self, u_obj, data):
    u_obj.organisations.add(self.organisation.pk)

  def assign_role(self, u_obj, data):
    for r in self.roles.values():
      u_obj.roles.remove(r)
    if data.get('role', None) == '1':
      u_obj.roles.add(self.roles['student'].pk)
    elif data.get('role', None) == '2':
      u_obj.roles.add(self.roles['teacher'].pk)
    elif data.get('role', None) == '3':
      u_obj.roles.add(self.roles['staff'].pk)

  def refresh_permissions(self, u_obj):
    udb_u = UserdbUser.objects.get(pk=u_obj.pk)
    udb_u.refresh_permissions()

  def create_usergroups(self, u_obj, data):
    u_obj.usergroups.clear()
    if data.get('description', False):
      ug, c = UserGroup.objects.get_or_create(name=data['description'])
      ug.users.add(u_obj)

  def create_wilma_profile(self, user, data):
    if not 'personal_identity_code_hash' in data or not 'role' in data:
      return None

    wilma_username = data['username'].partition('@')[0]
    if data.get('role', None) == '1':
      wilma_role = 'student'
    elif data.get('role', None) == '2':
      wilma_role = 'teacher'
    elif data.get('role', None) == '3':
      wilma_role = 'staff'
    else:
      return None

    for wilma_settings in WilmaSettings.objects.all():
      wu, c = WilmaUser.objects.get_or_create(user=user, wilma_settings=wilma_settings, defaults={'username': wilma_username, 'role': wilma_role, 'personal_identity_code_hash': data['personal_identity_code_hash']})
      if not c:
        if wu.username != wilma_username or wu.role != wilma_role or wu.personal_identity_code_hash != data['personal_identity_code_hash']:
          wu.username = wilma_username
          wu.role = wilma_role
          wu.personal_identity_code_hash = data['personal_identity_code_hash']
          wu.save()

  def create_dikaios_profile(self, u_obj, data):
    if data.get('school_code', None) is not None:
      school_code = data.get('school_code', None)
      if not school_code:
        self.stdout.write(u'Dikaios: Missing school code for user: %s\n' % data['username'])
      if self.city_code and school_code:
        dp, c = DikaiosProfile.objects.get_or_create(user_id=u_obj.pk, defaults={'school': school_code, 'city': self.city_code})
        if not c:
          dp.school = school_code
          dp.city = self.city_code
          dp.save()


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

