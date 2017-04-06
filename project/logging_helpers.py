# -*- coding: utf-8 -*-
#
# Copyright Haltu Oy, info@haltu.fi
# Licensed under the EUPL v1.1
#

import json

class Filter:
  def filter(self, record):
    if not 'data' in record.__dict__:
      record.__dict__['data'] = None
    record.__dict__['data'] = json.dumps(record.__dict__['data'], sort_keys=True, indent=2)
    return True

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

