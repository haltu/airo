# -*- coding: utf-8 -*-
#
# Copyright Haltu Oy, info@haltu.fi
# Licensed under the EUPL v1.1
#

import logging
import requests
from moodle.settings import API_KEY, ENDPOINT

LOG = logging.getLogger(__name__)


def fetch_users():
  """Do web request to moodle

  returns list of dicts where dict has keys username, first_name, last_name, email

  """
  # We are using core_user_get_users web function. If there are problems,
  # consider using 'core_enrol_get_enrolled_users' instead
  data = {}
  data['wstoken'] = API_KEY
  data['wsfunction'] = 'core_user_get_users'
  data['moodlewsrestformat'] = 'json'
  data['criteria[0][key]'] = 'all'
  data['criteria[0][value]'] = 'all'

  response = requests.post(ENDPOINT, data)

  try:
    response = response.json()
  except ValueError:
    LOG.error('Moodle did not return json content',
        extra={'data': {'response.text': response.text,
                        'status_code': response.status_code,
                        'API_KEY': API_KEY,
                        'ENDPOINT': ENDPOINT,
                        }})

  LOG.debug('Got data from %s' % ENDPOINT, extra={'data': {'response': response}})

  try:
    return response['users']
  except KeyError:
    LOG.error('Moodle response did not have users', extra={'data': {'response': response}})
    return []

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

