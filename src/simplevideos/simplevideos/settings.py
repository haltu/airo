# -*- coding: utf-8 -*-
#
# Copyright Haltu Oy, info@haltu.fi
# Licensed under the EUPL v1.1
#

from django.conf import settings

GOOGLE_API_KEY = getattr(settings, 'SIMPLEVIDEOS_GOOGLE_API_KEY', '')
REQUIRE_LOGIN = getattr(settings, 'SIMPLEVIDEOS_REQUIRE_LOGIN', False)
PLAYLIST_MAX_VIDEOS = getattr(settings, 'SIMPLEVIDEOS_PLAYLIST_MAX_VIDEOS', 200)
PLAYLIST_CACHE_EXPIRY = getattr(settings, 'SIMPLEVIDEOS_PLAYLIST_CACHE_EXPIRY', 60)
VIDEO_CACHE_EXPIRY = getattr(settings, 'SIMPLEVIDEOS_VIDEO_CACHE_EXPIRY', 60)

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

