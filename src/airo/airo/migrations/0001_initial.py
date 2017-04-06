# -*- coding: utf-8 -*-
#
# Copyright Haltu Oy, info@haltu.fi
# Licensed under the EUPL v1.1
#

from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Airo'
        db.create_table('airo_airo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('airo', ['Airo'])


    def backwards(self, orm):
        # Deleting model 'Airo'
        db.delete_table('airo_airo')


    models = {
        'airo.airo': {
            'Meta': {'object_name': 'Airo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['airo']

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

