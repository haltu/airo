# -*- coding: utf-8 -*-
#
# Copyright Haltu Oy, info@haltu.fi
# Licensed under the EUPL v1.1
#

import logging
import uuid
import hmac
import hashlib
from django.utils.http import urlquote_plus
from base64 import b64encode

LOG = logging.getLogger(__name__)


def get_random_string():
  return str(uuid.uuid4())


def check_nonce(nonce):
  length_ok = len(nonce) >= 16 and len(nonce) <= 40
  if not length_ok:
    LOG.warning('Nonce length not 16-40', extra={'data': {'nonce': nonce}})
  return length_ok


def calculate_checksum(password, content, encode=False):
  """Checksum is calculated as Base64-encoded HMAC-SHA1 hash"""
  hmac_obj = hmac.HMAC(key=str(password), msg=content.encode('utf-8'), digestmod=hashlib.sha1)
  checksum = b64encode(hmac_obj.digest())
  if encode:
    checksum = urlquote_plus(checksum)
  LOG.debug('HMAC-SHA1 checksum',
      extra={'data': {'content': content, 'checksum': checksum}})
  return checksum


def verify_checksum(password, content, checksum):
  our_checksum = calculate_checksum(password, content)
  # TODO: We should use hmac.compare_digest to prevent timing analysis attack
  checksum_ok = our_checksum == checksum
  if not checksum_ok:
    LOG.error('Wilma checksum error',
        extra={'data': {'our checksum': our_checksum, 'their checksum': checksum}})
  return checksum_ok


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

