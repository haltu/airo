# -*- coding: utf-8 -*-
#
# Copyright Haltu Oy, info@haltu.fi
# Licensed under the EUPL v1.1
#

from django.contrib import admin
from moodle.models import MoodleUser


class MoodleUserAdmin(admin.ModelAdmin):
  list_display = ('user', 'moodle_id')
  raw_id_fields = ('user',)
  search_fields = ('user__username', 'moodle_id')

admin.site.register(MoodleUser, MoodleUserAdmin)

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

