# -*- coding: utf-8 -*-
#
# Copyright Haltu Oy, info@haltu.fi
# Licensed under the EUPL v1.1
#

import logging
import requests
from django.core.cache import cache
from django.http import Http404
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView
from simplevideos import settings
from urlparse import parse_qs, urlparse

LOG = logging.getLogger(__name__)


def _parse_url(url):
  if not url.startswith('http'):
    url = '//' + url
  parsed = urlparse(url)
  query = parse_qs(parsed.query, keep_blank_values=True)
  return parsed, query


class YouTubeMixin(object):
  def get_youtube_playlist(self, id):
    r = requests.get('https://www.googleapis.com/youtube/v3/playlists', params={
      'part': 'snippet',
      'id': id,
      'key': settings.GOOGLE_API_KEY,
    })
    if r.status_code != 200:
      LOG.error('YouTube API error', extra={'request': r})
      raise Http404
    data = r.json()
    try:
      playlist = data['items'][0]
    except IndexError:
      LOG.error('YouTube API empty result', extra={'request': r})
      raise Http404
    return playlist

  def get_youtube_video(self, id):
    r = requests.get('https://www.googleapis.com/youtube/v3/videos', params={
      'part': 'snippet',
      'id': id,
      'key': settings.GOOGLE_API_KEY,
    })
    if r.status_code != 200:
      LOG.error('YouTube API error', extra={'request': r})
      raise Http404
    data = r.json()
    try:
      video = data['items'][0]
    except IndexError:
      LOG.error('YouTube API empty result', extra={'request': r})
      raise Http404
    return video


class CreateView(YouTubeMixin, TemplateView):
  template_name = 'simplevideos/create.html'

  def get_context_data(self, **kwargs):
    context = {
      'form_error': getattr(self, 'form_error', None)
    }
    return context

  def post(self, request, *args, **kwargs):
    url = request.POST.get('url', None)
    if url:
      playlist_id = self._get_playlist_id_from_url(url)
      video_id = self._get_video_id_from_url(url)
      try:
        if playlist_id:
          playlist = self.get_youtube_playlist(playlist_id)
        if video_id:
          video = self.get_youtube_video(video_id)
      except Http404:
        self.form_error = {
          'name': 'youtube_error',
          'display': _(u'The video or playlist is not available'),
        }
        return self.get(request, *args, **kwargs)
      if playlist_id and video_id:
        return redirect('simplevideos.video', playlist_id=playlist_id, id=video_id)
      if video_id:
        return redirect('simplevideos.video', id=video_id)
      if playlist_id:
        return redirect('simplevideos.playlist', id=playlist_id)
      self.form_error = {
        'name': 'id_parsing_error',
        'display': _(u'No video or playlist could be found'),
      }
    return self.get(request, *args, **kwargs)

  def _get_playlist_id_from_url(self, url):
    parsed, query = _parse_url(url)
    return query.get('list', [None,])[0]

  def _get_video_id_from_url(self, url):
    parsed, query = _parse_url(url)
    if parsed.netloc == 'youtu.be':
      return parsed.path[1:]
    else:
      return query.get('v', [None,])[0]


class PlaylistView(YouTubeMixin, TemplateView):
  template_name = 'simplevideos/playlist.html'

  def get_context_data(self, **kwargs):
    playlist_id = self.kwargs.get('id', None)
    videos = []
    page = None

    cached = cache.get('simplevideos_playlist_%s' % playlist_id)
    if cached:
      return cached

    playlist = self.get_youtube_playlist(playlist_id)

    while True:
      r = requests.get('https://www.googleapis.com/youtube/v3/playlistItems', params={
        'part': 'snippet',
        'maxResults': 50,
        'playlistId': playlist_id,
        'key': settings.GOOGLE_API_KEY,
        'pageToken': page,
      })
      if r.status_code != 200:
        LOG.error('YouTube API error', extra={'request': r})
        raise Http404
      data = r.json()
      videos.extend(data['items'])
      if len(videos) >= settings.PLAYLIST_MAX_VIDEOS:
        break
      if 'nextPageToken' in data:
        page = data['nextPageToken']
        continue
      break

    context = {
      'playlist': playlist,
      'videos': videos,
    }

    cache.set('simplevideos_playlist_%s' % playlist_id, context, settings.PLAYLIST_CACHE_EXPIRY)

    return context


class VideoView(YouTubeMixin, TemplateView):
  template_name = 'simplevideos/video.html'

  def get_context_data(self, **kwargs):
    video_id = self.kwargs.get('id', None)
    playlist_id = self.kwargs.get('playlist_id', None)

    cached = cache.get('simplevideos_video_%s_%s' % (video_id, playlist_id or ''))
    if cached:
      return cached

    if playlist_id:
      playlist = self.get_youtube_playlist(playlist_id)
    else:
      playlist = None

    video = self.get_youtube_video(video_id)

    context = {
      'video': video,
      'playlist': playlist,
    }

    cache.set('simplevideos_video_%s_%s' % (video_id, playlist_id or ''), context, settings.VIDEO_CACHE_EXPIRY)

    return context


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

