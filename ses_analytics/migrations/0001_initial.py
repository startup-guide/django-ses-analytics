# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Email'
        db.create_table(u'ses_analytics_email', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('from_email', self.gf('django.db.models.fields.EmailField')(max_length=75, db_index=True)),
            ('to_email', self.gf('django.db.models.fields.EmailField')(max_length=75, db_index=True)),
            ('raw_msg', self.gf('django.db.models.fields.TextField')()),
            ('hash', self.gf('django.db.models.fields.CharField')(max_length=30, db_index=True)),
            ('campaign', self.gf('django.db.models.fields.CharField')(max_length=20, db_index=True)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='sending', max_length=9, db_index=True)),
            ('is_read', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('read_time', self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True)),
            ('error', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'ses_analytics', ['Email'])


    def backwards(self, orm):
        # Deleting model 'Email'
        db.delete_table(u'ses_analytics_email')


    models = {
        u'ses_analytics.email': {
            'Meta': {'object_name': 'Email'},
            'campaign': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_index': 'True'}),
            'error': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'from_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'db_index': 'True'}),
            'hash': ('django.db.models.fields.CharField', [], {'max_length': '30', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'raw_msg': ('django.db.models.fields.TextField', [], {}),
            'read_time': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'sending'", 'max_length': '9', 'db_index': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'to_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'db_index': 'True'})
        }
    }

    complete_apps = ['ses_analytics']