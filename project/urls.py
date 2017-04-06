# -*- coding: utf-8 -*-
#
# Copyright Haltu Oy, info@haltu.fi
# Licensed under the EUPL v1.1
#

from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.simple import redirect_to
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.conf import settings
from dreamcards.views import set_language
from airo.useradmin import site as useradmin

from django.contrib import admin
admin.autodiscover()

handler500  # Pyflakes

urlpatterns = patterns('',
  (r'^sysadmin/?', include(admin.site.urls)),
  (r'^useradmin/?', include(useradmin.urls)),
  url(r'^set_language/$', login_required(set_language), name='set_language'),
  url('^login/$', 'shibboleth.views.login', name='login'),
  (r'^', include('dreamcards.urls.desktop')),
  (r'^uiapi/1/', include('dreamcards.urls.uiapi')),
  (r'^', include('airo.urls')),
  (r'^wilma/', include('wilma.urls')),
  (r'^v/', include('simplevideos.urls')),
  (r'^dikaios/', include('dreamdikaios.dreamdikaiosdreamcards.urls')),
  #(r'^404/$', TemplateView.as_view(template_name='404.html')),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

