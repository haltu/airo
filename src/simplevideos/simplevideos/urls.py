# -*- coding: utf-8 -*-
#
# Copyright Haltu Oy, info@haltu.fi
# Licensed under the EUPL v1.1
#

from django.conf.urls import patterns, url
from simplevideos import settings
from simplevideos.views import CreateView, PlaylistView, VideoView

if settings.REQUIRE_LOGIN:
  from django.contrib.auth.decorators import login_required
  create_view = login_required(CreateView.as_view())
  playlist_view = login_required(PlaylistView.as_view())
  video_view = login_required(VideoView.as_view())
else:
  create_view = CreateView.as_view()
  playlist_view = PlaylistView.as_view()
  video_view = VideoView.as_view()

urlpatterns = patterns('',
  url(r'^create/?$', create_view, name='simplevideos.create'),
  url(r'^playlist/(?P<id>[^/]+)/?$', playlist_view, name='simplevideos.playlist'),
  url(r'^playlist/(?P<playlist_id>[^/]+)/video/(?P<id>[^/]+)/?$', video_view, name='simplevideos.video'),
  url(r'^video/(?P<id>[^/]+)/?$', video_view, name='simplevideos.video'),
)

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

