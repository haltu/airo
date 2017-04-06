# -*- coding: utf-8 -*-
#
# Copyright Haltu Oy, info@haltu.fi
# Licensed under the EUPL v1.1
#

import logging
from django.core.management.base import BaseCommand
from dreamcards.models import Card, Page, CardPageAssociation

LOG = logging.getLogger(__name__)


class Command(BaseCommand):
  help = 'Attach default cards to empty pages'

  def handle(self, *args, **options):
    self.cards = Card.objects.filter(default_for_new_users=True, owner__isnull=True)
    self.stdout.write('Starting to attach default cards: %s\n'%', '.join([str(card) for card in self.cards]))
    for page in Page.objects.filter(cardpageassociation__isnull=True):
      self.stdout.write('Attaching to page %s\n'%str(page))
      order = 0
      for card in self.cards:
        order += 1
        CardPageAssociation.objects.create(page=page, card=card, order=order)
    self.stdout.write('Done.\n')


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

