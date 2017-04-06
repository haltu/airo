# -*- coding: utf-8 -*-
#
# Copyright Haltu Oy, info@haltu.fi
# Licensed under the EUPL v1.1
#

"""Single-Sign-On to Wilma

.. note: This is from Wilma documentation

Wilma does also support Single-Sign-On from an external site. It should be
noted, that Wilma contains a lot of sensitive and personal information about
users. SSO should only be allowed from secure parners. A less secure or less
critical site should not be relied on as a SSO identity provider.

 * User logs on to the external site

 * The external site provides a link to Wilma:
   https://wilma.xxxx.fi/login?ssokey=xxx&query=https://yyy&logout=https://zzz&nonce=xyxyxy&h=nnn

 * Link contains:
    - ssokey=Unique single-sign-on-key, which the external site generates for an authenticated user.
    - query=URL, that Wilma must call for more information about the ssokey provided.
    - logout=URL, that the external site wants Wilma to call, when the user logs off Wilma
    - nonce=16-40 characters of random text.
    - h=Checksum , calculated from the following part of the URL:
      - ssokey=xxx&query=https://yyy&logout=https://zzz&nonce=xyxyxy

 * Wilma checks, that:
    - The query URL is registered as a trusted SSO query URL in Wilma.
    - Nonce is 16-40 characters.
    - The hash is correct.

 * Wilma calls the query-url, that the external site provided in the previous URL:
    https://xsite/xsitequery?ssokey=xxx&logout=https://zzz&nonce=xyxyxy&h=nnn

 * Parameters are:
   - ssokey=The ssokey, from the previous URL.
   - logout=URL, that Wilma wants the external site to call, when the user logs off the external site.
   - nonce=16-40 characters of random text.
   - h=Checksum calculated from the following part of the URL:
       ssokey=xxx&logout=https://zzz&nonce=xyxyxy

 * The external site must check, that:
   - Nonce is 16-40 characters.
   - The hash is correct.
   - A user with the ssokey is logged on in the external site.

 * The external site returns a UTF-8 encoded page containing:
  - ssokey=The ssokey, that was provided in the URL.
  - orignonce=The nonce, that was provided by Wilma.
  - nonce=16-40 characters of random text.
  - login=Username on the external site.

 * For each role, that the user has on the external site:
  - name=Name of user.
  - role=Role of user (teacher, student, staff or guardian)
  - uniqueid=Base64-encoded HMAC-SHA1 hash, calculated from user's "encrypted" social security id
  - using nonce as a key.
  - h=Checksum calculated from all the previous lines, using a shared secret as a key.

 * Wilma checks, that:
  - Orignonce and ssokey matches with the query URL that Wilma sent to the external site.
  - Nonce is 16-40 characters.
  - The hash is correct.
  - Login is found in Wilma.
  - Role is correct.
  - Uniqueid matches to the Base64-encoded HMAC-SHA1 hash, that Wilma
    calculates from user's "encrypted" social security id.

"""

import logging
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
import wilma.utils
import wilma.models
from wilma.settings import SESSION_COOKIE_NAME

LOG = logging.getLogger(__name__)


@login_required
def wilma_login_redirect(request, wilma_pk):
  try:
    wilma_settings = wilma.models.WilmaSettings.objects.get(pk=wilma_pk)
    wilma_profile = wilma.models.WilmaUser.objects.get(user=request.user, wilma_settings=wilma_settings)
  except wilma.models.WilmaSettings.DoesNotExist:
    raise Http404
  except wilma.models.WilmaUser.DoesNotExist:
    return HttpResponseRedirect(wilma_settings.server_url)
  url = wilma_profile.get_sso_url(session_key=request.COOKIES.get(SESSION_COOKIE_NAME, None))
  LOG.debug('Wilma login url for user %s' % request.user.pk,
      extra={'data': {'url': url,
                      'wilma_username': wilma_profile.username,
                      'wilma_role': wilma_profile.role,
                      'wilma_server_url': wilma_settings.server_url,
                      }})
  return HttpResponseRedirect(url)


def wilma_query(request, wilma_pk, session_key=None):
  LOG.debug('Processing wilma query. Request made by Wilma backend',
      extra={'data': {'wilma_pk': wilma_pk,
        'POST': dict(request.POST),
        'GET': dict(request.GET)}
        }
  )
  wilma_settings = get_object_or_404(wilma.models.WilmaSettings, pk=wilma_pk)

  c = {}  # context
  c['ssokey'] = request.GET.get('ssokey', '')
  c['slourl'] = request.GET.get('logout', '')  # This url should be called when user logs out from desktoplite
  c['orignonce'] = request.GET.get('nonce', '')
  c['checksum'] = request.GET.get('h', '')  # calculated from ssokey=xxx&logout=https://zzz&nonce=zyzyzy

  # Seems that Wilma does not properly URL-encode the parameters. Base64 data can contain '+' characters that are converted to spaces.
  # This is a hack to circumvent Wilma bug.
  if ' ' in c['checksum']:
    c['checksum'] = c['checksum'].replace(' ', '+')

  # Check that orignonce is 16-40 characters
  if not wilma.utils.check_nonce(c['orignonce']):
    LOG.error('Wilma SSO failed', extra={'data': {'error': 'Nonce check failed', 'ssokey': c['ssokey'], 'logout': c['slourl'], 'nonce': c['orignonce'], 'checksum': c['checksum']}})
    return HttpResponseBadRequest('nonce error')
  LOG.debug('nonce OK')

  # Check that hash is correct
  checksum_content = 'ssokey=%(ssokey)s&logout=%(slourl)s&nonce=%(orignonce)s' % c
  password = wilma_settings.sso_secret
  if not wilma.utils.verify_checksum(password, checksum_content, c['checksum']):
    LOG.error('Wilma SSO failed', extra={'data': {'error': 'Checksum failed', 'checksum_content': checksum_content, 'ssokey': c['ssokey'], 'logout': c['slourl'], 'nonce': c['orignonce'], 'checksum': c['checksum']}})
    return HttpResponseBadRequest('checksum error')
  LOG.debug('checksum OK')

  try:
    wilma_profile = wilma.models.WilmaUser.objects.get(ssokey=c['ssokey'])
  except wilma.models.WilmaUser.DoesNotExist:
    LOG.error('Wilma SSO failed', extra={'data': {'error': 'No user with provided ssokey found', 'ssokey': c['ssokey'], 'logout': c['slourl'], 'nonce': c['orignonce'], 'checksum': c['checksum']}})
    raise Http404

  LOG.debug('user object found')

  c['nonce'] = wilma.utils.get_random_string()
  c['login'] = wilma_profile.username

  LOG.debug('creating parameters')
  parameters = []
  parameters.append(u'ssokey=%(ssokey)s' % c)
  parameters.append(u'orignonce=%(orignonce)s' % c)
  parameters.append(u'nonce=%(nonce)s' % c)
  parameters.append(u'login=%(login)s' % c)
  LOG.debug('getting role list for user')
  try:
    parameters += wilma_profile.get_role_list(c['nonce'])
  except Exception:
    LOG.debug('parameters', extra={'data': {'c': c, 'parameters': parameters}})
    LOG.exception('could not get roles for user')

  return_rendered = u"\r\n".join(parameters) + u"\r\n"

  LOG.debug('calculating checksum')
  h = wilma.utils.calculate_checksum(password, return_rendered, encode=False)
  return_rendered = return_rendered + u'h=' + h
  LOG.debug('return rendered OK')

  LOG.debug('response to wilma query', extra={'data': {'return_rendered': repr(return_rendered), 'context': c, 'h': repr(h)}})

  res = HttpResponse(return_rendered)
  res['Content-Length'] = len(res.content)
  return res

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

