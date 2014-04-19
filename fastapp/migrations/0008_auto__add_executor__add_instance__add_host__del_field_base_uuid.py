# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Executor'
        db.create_table(u'fastapp_executor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('base', self.gf('django.db.models.fields.related.ForeignKey')(related_name='executor', to=orm['fastapp.Base'])),
            ('pid', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'fastapp', ['Executor'])

        # Adding model 'Instance'
        db.create_table(u'fastapp_instance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('is_alive', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('last_beat', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('executor', self.gf('django.db.models.fields.related.ForeignKey')(related_name='instances', to=orm['fastapp.Executor'])),
        ))
        db.send_create_signal(u'fastapp', ['Instance'])

        # Adding model 'Host'
        db.create_table(u'fastapp_host', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'fastapp', ['Host'])

        # Deleting field 'Base.uuid'
        db.delete_column(u'fastapp_base', 'uuid')


    def backwards(self, orm):
        # Deleting model 'Executor'
        db.delete_table(u'fastapp_executor')

        # Deleting model 'Instance'
        db.delete_table(u'fastapp_instance')

        # Deleting model 'Host'
        db.delete_table(u'fastapp_host')

        # Adding field 'Base.uuid'
        db.add_column(u'fastapp_base', 'uuid',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=36, blank=True),
                      keep_default=False)


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'fastapp.apy': {
            'Meta': {'object_name': 'Apy'},
            'base': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'apys'", 'null': 'True', 'to': u"orm['fastapp.Base']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module': ('django.db.models.fields.CharField', [], {'default': "'def func(self):\\n    pass'", 'max_length': '8192'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'fastapp.authprofile': {
            'Meta': {'object_name': 'AuthProfile'},
            'access_token': ('django.db.models.fields.CharField', [], {'max_length': '72'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'authprofile'", 'unique': 'True', 'to': u"orm['auth.User']"})
        },
        u'fastapp.base': {
            'Meta': {'object_name': 'Base'},
            'content': ('django.db.models.fields.CharField', [], {'default': '\'{% extends "fastapp/index.html" %}\\n{% block content %}\\n{% endblock %}\\n\'', 'max_length': '8192', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'+'", 'blank': 'True', 'to': u"orm['auth.User']"})
        },
        u'fastapp.counter': {
            'Meta': {'object_name': 'Counter'},
            'apy': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'counter'", 'unique': 'True', 'to': u"orm['fastapp.Apy']"}),
            'executed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'failed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'fastapp.executor': {
            'Meta': {'object_name': 'Executor'},
            'base': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'executor'", 'to': u"orm['fastapp.Base']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pid': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'fastapp.host': {
            'Meta': {'object_name': 'Host'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'fastapp.instance': {
            'Meta': {'object_name': 'Instance'},
            'executor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'instances'", 'to': u"orm['fastapp.Executor']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_alive': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_beat': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'})
        },
        u'fastapp.setting': {
            'Meta': {'object_name': 'Setting'},
            'base': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'setting'", 'to': u"orm['fastapp.Base']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '8192'})
        }
    }

    complete_apps = ['fastapp']