# -*- coding: utf-8 -*-
#
# Copyright Haltu Oy, info@haltu.fi
# Licensed under the EUPL v1.1
#

from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from django.db import connection

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Don't use "from appname.models import ModelName". 
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.

        for c in orm['desktoplite.Category'].objects.all():
            owner_id = None
            if c.owner:
                owner_id = c.owner.id

            category = orm['dreamcards.Category'](
                    pk=c.pk,
                    title=c.title,
                    owner_id=owner_id,
                    active=c.active,
                    language=c.language)
            category.save()

        cursor = connection.cursor()
        cursor.execute("SELECT setval('dreamcards_category_id_seq', (SELECT MAX(id) FROM dreamcards_category))")
        cursor.close()

        for g in orm['desktoplite.UserGroup'].objects.all():
            ug = orm['dreamcards.UserGroup'](
                    pk=g.pk,
                    name=g.name,
                )
            ug.save()
            ug.users.add(*g.users.all().values_list('pk', flat=True))

        cursor = connection.cursor()
        cursor.execute("SELECT setval('dreamcards_usergroup_id_seq', (SELECT MAX(id) FROM dreamcards_usergroup))")
        cursor.close()

        for c in orm['desktoplite.Card'].objects.all():
            owner_id = None
            if c.owner:
                owner_id = c.owner.id

            category_id = None
            if c.category:
                category_id = c.category.id

            card = orm['dreamcards.Card'](
                pk=c.pk,
                title=c.title,
                url=c.url,
                thumbnail=c.thumbnail,
                category_id=category_id,
                owner_id=owner_id,
                active=c.active,
                card_type=c.card_type,
                language=c.language,
                default_for_new_users=c.default_for_new_users,
            )
            card.save()
            card.groups.add(*c.groups.all().values_list('id', flat=True))
            card.users.add(*c.users.all().values_list('id', flat=True))

        cursor = connection.cursor()
        cursor.execute("SELECT setval('dreamcards_card_id_seq', (SELECT MAX(id) FROM dreamcards_card))")
        cursor.close()


        for p in orm['desktoplite.Page'].objects.all():
            owner_id = None
            if p.owner:
                owner_id = p.owner.id

            page = orm['dreamcards.Page'](
                    pk=p.pk,
                    title=p.title,
                    owner_id=owner_id,
                    active=p.active,
                )
            page.save()
            # cards comes in CardPageAssociation migration
            #page.cards.add(*p.cards.all().values_list('id', flat=True))

        cursor = connection.cursor()
        cursor.execute("SELECT setval('dreamcards_page_id_seq', (SELECT MAX(id) FROM dreamcards_page))")
        cursor.close()

        for cpa in orm['desktoplite.CardPageAssociation'].objects.all():
            association = orm['dreamcards.CardPageAssociation'](
                        pk=cpa.pk,
                        card_id=cpa.card.id,
                        page_id=cpa.page.id,
                        size_x=cpa.size_x,
                        size_y=cpa.size_y,
                        order=cpa.order,
                    )
            association.save()

        cursor = connection.cursor()
        cursor.execute("SELECT setval('dreamcards_cardpageassociation_id_seq', (SELECT MAX(id) FROM dreamcards_cardpageassociation))")
        cursor.close()


        for up in orm['desktoplite.UserProfile'].objects.all():
            profile = orm['dreamcards.DesktopUserProfile'](
                    pk=up.pk,
                    user_id=up.user.id,
                    preferred_background=up.preferred_background,
                    preferred_language=up.preferred_language,
                )
            profile.save()

        cursor = connection.cursor()
        cursor.execute("SELECT setval('dreamcards_desktopuserprofile_id_seq', (SELECT MAX(id) FROM dreamcards_desktopuserprofile))")
        cursor.close()



    def backwards(self, orm):
        "Write your backwards methods here."
        raise NotImplementedError('backwards not implemented')

    models = {
        'airo.airo': {
            'Meta': {'object_name': 'Airo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2048'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'desktoplite.card': {
            'Meta': {'object_name': 'Card'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'card_type': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'cards'", 'null': 'True', 'to': "orm['desktoplite.Category']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'default_for_new_users': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['desktoplite.UserGroup']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'foo2'", 'null': 'True', 'to': "orm['auth.User']"}),
            'permission': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'foo'", 'null': 'True', 'to': "orm['auth.Permission']"}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '4096'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'foo1'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['auth.User']"})
        },
        'desktoplite.cardpageassociation': {
            'Meta': {'unique_together': "(('page', 'card'),)", 'object_name': 'CardPageAssociation'},
            'card': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'page_associations'", 'to': "orm['desktoplite.Card']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'card_associations'", 'to': "orm['desktoplite.Page']"}),
            'size_x': ('django.db.models.fields.PositiveIntegerField', [], {'default': '2'}),
            'size_y': ('django.db.models.fields.PositiveIntegerField', [], {'default': '2'})
        },
        'desktoplite.category': {
            'Meta': {'object_name': 'Category'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'foo'", 'null': 'True', 'to': "orm['auth.User']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '4096'})
        },
        'desktoplite.desktoplite': {
            'Meta': {'object_name': 'DesktopLite'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'desktoplite.page': {
            'Meta': {'object_name': 'Page'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'cards': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'on_pages'", 'to': "orm['desktoplite.Card']", 'through': "orm['desktoplite.CardPageAssociation']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'foo3'", 'null': 'True', 'to': "orm['auth.User']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '4096'})
        },
        'desktoplite.usergroup': {
            'Meta': {'ordering': "('name',)", 'object_name': 'UserGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'foo4'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['auth.User']"})
        },
        'desktoplite.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'preferred_background': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'preferred_language': ('django.db.models.fields.CharField', [], {'default': "'fi'", 'max_length': '2'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'dreamcards.card': {
            'Meta': {'object_name': 'Card'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'card_type': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'cards'", 'null': 'True', 'to': "orm['dreamcards.Category']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'default_for_new_users': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['dreamcards.UserGroup']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dreamsso.User']", 'null': 'True', 'blank': 'True'}),
            'permission': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.Permission']", 'null': 'True', 'blank': 'True'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '4096'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'directly_shared_cards'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['dreamsso.User']"})
        },
        'dreamcards.cardpageassociation': {
            'Meta': {'unique_together': "(('page', 'card'),)", 'object_name': 'CardPageAssociation'},
            'card': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'page_associations'", 'to': "orm['dreamcards.Card']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'card_associations'", 'to': "orm['dreamcards.Page']"}),
            'size_x': ('django.db.models.fields.PositiveIntegerField', [], {'default': '2'}),
            'size_y': ('django.db.models.fields.PositiveIntegerField', [], {'default': '2'})
        },
        'dreamcards.category': {
            'Meta': {'object_name': 'Category'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'color': ('django.db.models.fields.CharField', [], {'default': "'grey'", 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dreamsso.User']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '4096'})
        },
        'dreamcards.desktopuserprofile': {
            'Meta': {'object_name': 'DesktopUserProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'preferred_background': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'preferred_language': ('django.db.models.fields.CharField', [], {'default': "'fi'", 'max_length': '2'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['dreamsso.User']", 'unique': 'True'})
        },
        'dreamcards.dreamcards': {
            'Meta': {'object_name': 'DreamCards'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'dreamcards.page': {
            'Meta': {'object_name': 'Page'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'cards': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'on_pages'", 'to': "orm['dreamcards.Card']", 'through': "orm['dreamcards.CardPageAssociation']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'pages'", 'null': 'True', 'to': "orm['dreamsso.User']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '4096'})
        },
        'dreamcards.usergroup': {
            'Meta': {'ordering': "('name',)", 'object_name': 'UserGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'usergroups'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['dreamsso.User']"})
        },
        'dreamsso.group': {
            'Meta': {'ordering': "['name', 'title']", 'unique_together': "(('name', 'organisation'),)", 'object_name': 'Group', 'db_table': "'dreamuserdb_group'", 'managed': 'False'},
            'filter_type': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'official': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'organisation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dreamsso.Organisation']"}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['dreamsso.Group']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'dreamsso.organisation': {
            'Meta': {'ordering': "['title', 'name']", 'object_name': 'Organisation', 'db_table': "'dreamuserdb_organisation'", 'managed': 'False'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'dreamsso.role': {
            'Meta': {'ordering': "['name', 'title']", 'unique_together': "(('name', 'organisation'),)", 'object_name': 'Role', 'db_table': "'dreamuserdb_role'", 'managed': 'False'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'official': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'organisation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dreamsso.Organisation']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'dreamsso.user': {
            'Meta': {'ordering': "['username']", 'managed': 'False', 'object_name': 'User', 'db_table': "'dreamuserdb_user'", '_ormbases': ['auth.User']},
            'active_organisation': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'active_users'", 'null': 'True', 'to': "orm['dreamsso.Organisation']"}),
            'auth_user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'dreamsso_user'", 'unique': 'True', 'primary_key': 'True', 'to': "orm['auth.User']"}),
            'locale': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'organisations': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['dreamsso.Organisation']", 'symmetrical': 'False', 'blank': 'True'}),
            'personal_identity_code_hash': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'picture_url': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'profile_picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'roles': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['dreamsso.Role']", 'symmetrical': 'False', 'blank': 'True'}),
            'theme_color': ('django.db.models.fields.CharField', [], {'default': "'ffffff'", 'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'user_groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['dreamsso.Group']", 'symmetrical': 'False', 'blank': 'True'})
        }
    }

    complete_apps = ['desktoplite', 'dreamcards', 'airo']
    symmetrical = True

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

