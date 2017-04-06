# -*- coding: utf-8 -*-
#
# Copyright Haltu Oy, info@haltu.fi
# Licensed under the EUPL v1.1
#

from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
from django.contrib import admin
from django.contrib.auth.models import Permission
from django.http import HttpResponseRedirect
from dreamcards import models
from airo import settings


class UserAdminSite(admin.AdminSite):
  def has_permission(self, request):
    return request.user.is_active and request.user.has_perm('dreamcards.can_use_useradmin')

  def login(self, request, extra_context=None):
    # login via normal views is mandatory before using useradmin
    return HttpResponseRedirect('/')

site = UserAdminSite(name='useradmin')


class CategoryFilter(admin.SimpleListFilter):
  title = _('category')
  parameter_name = 'category'
  field_name = 'category'

  def lookup_queryset(self, request, model_admin):
    return models.Category.objects.filter(owner__isnull=True)

  def lookups(self, request, model_admin):
    lookups = [('none', _(u'None'))]
    lookups.extend([(str(c.id), unicode(c)) for c in self.lookup_queryset(request, model_admin)])
    return lookups

  def queryset(self, request, queryset):
    if self.value() == 'none':
      return queryset.filter(**{"%s__isnull"%self.field_name: True})
    elif self.value():
      return queryset.filter(**{"%s__id"%self.field_name: self.value()})


class CardAdmin(admin.ModelAdmin):
  list_display = ('thumbnail_tag', 'title', 'url', 'category', 'language',)
  list_display_links = list_display
  list_filter = ('language', CategoryFilter)
  search_fields = ('title', 'url', 'category__title')
  read_only_fields = ('thumbnail_tag',)
  exclude = ('card_type', 'active', 'owner', 'groups', 'users')

  def formfield_for_foreignkey(self, db_field, request, **kwargs):
    """
    Only system categories are selectable.
    """
    if db_field.name == 'category':
      kwargs['queryset'] = models.Category.objects.filter(owner__isnull=True)
    elif db_field.name == 'permission':
      filters = Q()
      for f in settings.USERADMIN_CARD_PERMISSION_FILTER:
        filters = filters | Q(content_type__app_label=f[0], content_type__model=f[1], codename=f[2])
      kwargs['queryset'] = Permission.objects.filter(filters)

    return super(CardAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

  def queryset(self, request):
    """
    Display only system cards.
    """
    qs = super(CardAdmin, self).queryset(request)
    return qs.filter(owner__isnull=True)


class CategoryAdmin(admin.ModelAdmin):
  list_display = ('title', 'language', 'card_list_link')
  list_filter = ('language',)
  search_fields = ('title',)
  exclude = ('active', 'owner')
  read_only_fields = ('number_of_cards',)

  def queryset(self, request):
    """
    Display only system categories.
    """
    qs = super(CategoryAdmin, self).queryset(request)
    return qs.filter(owner__isnull=True)

site.register(models.Card, CardAdmin)
site.register(models.Category, CategoryAdmin)


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

