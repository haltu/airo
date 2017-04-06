# -*- coding: utf-8 -*-
#
# Copyright Haltu Oy, info@haltu.fi
# Licensed under the EUPL v1.1
#

from django.contrib import admin
from wilma.models import WilmaUser, WilmaSettings


class WilmaUserAdmin(admin.ModelAdmin):
  list_display = ('user', 'ssokey', 'personal_identity_code_hash', 'username', 'role')
  raw_id_fields = ('user',)
  search_fields = ('username', 'personal_identity_code_hash', 'ssokey')
  list_filter = ('role',)


class WilmaSettingsAdmin(admin.ModelAdmin):
  list_display = ('server_url', 'sso_secret')


admin.site.register(WilmaUser, WilmaUserAdmin)
admin.site.register(WilmaSettings, WilmaSettingsAdmin)

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

