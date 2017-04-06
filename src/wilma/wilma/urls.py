# -*- coding: utf-8 -*-
#
# Copyright Haltu Oy, info@haltu.fi
# Licensed under the EUPL v1.1
#

from django.conf.urls import patterns, url

urlpatterns = patterns('wilma.views',
  url(r'^login/(?P<wilma_pk>\d+)/$', 'wilma_login_redirect', name='wilma.wilma_login_redirect'),
  url(r'^(?P<wilma_pk>\d+)/$', 'wilma_query', name='wilma.wilma_query'),
  url(r'^(?P<wilma_pk>\d+)/(?P<session_key>.*)/$', 'wilma_query', name='wilma.wilma_query'),
)

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

