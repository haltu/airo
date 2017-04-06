# -*- coding: utf-8 -*-
#
# Copyright Haltu Oy, info@haltu.fi
# Licensed under the EUPL v1.1
#

import logging
import requests
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, NoReverseMatch
from airo.signals import logout_initiated
import wilma.utils
import wilma.settings


LOG = logging.getLogger(__name__)

ROLE_CHOICES = (
  ('teacher', 'teacher'),
  ('student', 'student'),
  ('staff', 'staff'),
)


class WilmaUser(models.Model):
  user = models.ForeignKey(User, related_name='wilma')
  wilma_settings = models.ForeignKey('wilma.WilmaSettings')
  ssokey = models.CharField(max_length=40, blank=True, null=True)
  username = models.CharField(max_length=200, blank=True)
  role = models.CharField(max_length=200, choices=ROLE_CHOICES)
  personal_identity_code_hash = models.CharField(max_length=2048, blank=True, null=True)

  class Meta:
    verbose_name = u'Wilma user'
    verbose_name_plural = u'Wilma users'

  def __unicode__(self):
    return unicode(self.user)

  def get_ssokey(self):
    if not self.ssokey:
      self.ssokey = wilma.utils.get_random_string()
      self.save()
    return self.ssokey

  def get_uniqueid(self, nonce):
    if not self.personal_identity_code_hash:
      LOG.error('user does not have personal_identity_code_hash. Wilma login will fail', extra={'data': {'username': repr(self.user.username), 'user_id': self.user.pk}})
    return wilma.utils.calculate_checksum(nonce, self.personal_identity_code_hash, encode=False)

  def get_role_list(self, nonce):
    data = [u'name=%s' % u'foo',  # self.user.user.get_full_name(),
            u'role=%s' % self.role,
            u'uniqueid=%s' % self.get_uniqueid(nonce)
            ]
    return data

  def get_sso_url(self, session_key=None):
    d = {}
    d['url'] = self.wilma_settings.server_url.rstrip('/')
    d['ssokey'] = self.get_ssokey()
    d['query'] = self.wilma_settings.get_query_url(session_key)
    d['logout'] = self.wilma_settings.airo_logout_url
    d['nonce'] = wilma.utils.get_random_string()
    checksum_content = 'ssokey=%(ssokey)s&query=%(query)s&logout=%(logout)s&nonce=%(nonce)s' % d
    d['h'] = wilma.utils.calculate_checksum(self.wilma_settings.sso_secret, checksum_content, encode=True)
    sso_url = '%(url)s/login?ssokey=%(ssokey)s&query=%(query)s&logout=%(logout)s&nonce=%(nonce)s&h=%(h)s' % d
    d['sso_url'] = sso_url
    LOG.debug('wilma sso url for user %s' % self.user.pk, extra={'data': {'d': d, 'personal_id': self.personal_identity_code_hash}})
    return sso_url


class WilmaSettings(models.Model):
  """ Wilma service settings
  """
  server_url = models.URLField(max_length=2048, blank=True)
  logout_url = models.URLField(max_length=2048, blank=True)
  sso_secret = models.CharField(max_length=200, blank=True)

  class Meta:
    verbose_name = u'Wilma settings'
    verbose_name_plural = u'Wilma settings'

  def __unicode__(self):
    return self.server_url

  def get_query_url(self, session_key=None):
    """ Return query url to which wilma connects during sso authentication. Accepts user's session key for storing user-specific single logout url.
    """
    kwargs = {'wilma_pk': self.pk}
    if session_key is not None:
      kwargs.update({'session_key': session_key})
    return wilma.settings.BASE_URL + reverse('wilma.wilma_query', kwargs=kwargs)

  @property
  def airo_logout_url(self):
    try:
      return wilma.settings.BASE_URL + reverse('logout')
    except NoReverseMatch:
      return wilma.settings.BASE_URL + '/logout'


## Signal handlers

def handle_wilma_logout(sender, request, **kwargs):
  for wilmauser in sender.wilma.all():
    wilma_logout_url = wilmauser.wilma_settings.logout_url
    if wilma_logout_url:
      auth = "ssokey=%s&nonce=%s"%(wilmauser.get_ssokey(), wilma.utils.get_random_string())
      h = wilma.utils.calculate_checksum(wilmauser.wilma_settings.sso_secret, auth, encode=True)
      payload = auth + '&h=' + h
      headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
      }
      try:
        response = requests.post(wilma_logout_url, data=str(payload), headers=headers, timeout=10)
      except requests.exceptions.RequestException as e:
        LOG.error('Wilma SLO failed', exc_info=e, extra={'data': {'user': sender.pk}})
      if response.status_code != requests.codes.ok:
        LOG.error('Wilma SLO failed', extra={'data': {'user': sender.pk, 'response_status': response.status_code, 'response': response.text}})
      LOG.debug('Wilma SLO completed', extra={'data': {'user': sender.pk, 'wilma_response': response}})


logout_initiated.connect(handle_wilma_logout)

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

