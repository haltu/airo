# -*- coding: utf-8 -*-
#
# Copyright Haltu Oy, info@haltu.fi
# Licensed under the EUPL v1.1
#

from django.conf.urls import url, patterns, include
from rest_framework import routers
from dreamdikaios.dreamdikaiosdreamcards.views import EdustoreCardViewSet
from airo.views import logout_view


router = routers.DefaultRouter()
router.register(r'dreamcards/cards/edustorecard', EdustoreCardViewSet, base_name='cards_edustorecard')

urlpatterns = patterns('',
    url(r'logout$', logout_view, name='logout'),
    url(r'^uiapi/1/', include(router.urls)),
)

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

