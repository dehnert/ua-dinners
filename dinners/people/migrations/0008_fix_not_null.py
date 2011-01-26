# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'AthenaPerson.first_name'
        db.alter_column('people_athenaperson', 'first_name', self.gf('django.db.models.fields.CharField')(max_length=30, null=True))

        # Changing field 'AthenaPerson.mod_date'
        db.alter_column('people_athenaperson', 'mod_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True))

        # Changing field 'PersonType.mutable'
        db.alter_column('people_persontype', 'mutable', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'PersonType.student'
        db.alter_column('people_persontype', 'student', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'PersonType.faculty'
        db.alter_column('people_persontype', 'faculty', self.gf('django.db.models.fields.BooleanField')(blank=True))


    def backwards(self, orm):
        
        # Changing field 'AthenaPerson.first_name'
        db.alter_column('people_athenaperson', 'first_name', self.gf('django.db.models.fields.CharField')(max_length=30))

        # Changing field 'AthenaPerson.mod_date'
        db.alter_column('people_athenaperson', 'mod_date', self.gf('django.db.models.fields.DateField')())

        # Changing field 'PersonType.mutable'
        db.alter_column('people_persontype', 'mutable', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'PersonType.student'
        db.alter_column('people_persontype', 'student', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'PersonType.faculty'
        db.alter_column('people_persontype', 'faculty', self.gf('django.db.models.fields.BooleanField')())


    models = {
        'people.alumperson': {
            'Meta': {'object_name': 'AlumPerson'},
            'account_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '8'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'grad_year': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'people.athenaperson': {
            'Meta': {'object_name': 'AthenaPerson'},
            'add_date': ('django.db.models.fields.DateField', [], {}),
            'del_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'krb_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '8'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'mod_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'office_location': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'person_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.PersonType']"}),
            'unit_name': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True'}),
            'year': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'})
        },
        'people.persontype': {
            'Meta': {'object_name': 'PersonType'},
            'faculty': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mutable': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'student': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'})
        }
    }

    complete_apps = ['people']
