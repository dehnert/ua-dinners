# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'AthenaPerson.unit_name'
        db.alter_column('people_athenaperson', 'unit_name', self.gf('django.db.models.fields.CharField')(max_length=45, null=True))

        # Changing field 'AthenaPerson.office_location'
        db.alter_column('people_athenaperson', 'office_location', self.gf('django.db.models.fields.CharField')(max_length=30, null=True))

        # Changing field 'AthenaPerson.year'
        db.alter_column('people_athenaperson', 'year', self.gf('django.db.models.fields.CharField')(max_length=1, null=True))


    def backwards(self, orm):
        
        # Changing field 'AthenaPerson.unit_name'
        db.alter_column('people_athenaperson', 'unit_name', self.gf('django.db.models.fields.CharField')(default='', max_length=45))

        # Changing field 'AthenaPerson.office_location'
        db.alter_column('people_athenaperson', 'office_location', self.gf('django.db.models.fields.CharField')(default='', max_length=30))

        # Changing field 'AthenaPerson.year'
        db.alter_column('people_athenaperson', 'year', self.gf('django.db.models.fields.CharField')(default='', max_length=1))


    models = {
        'people.alumperson': {
            'Meta': {'object_name': 'AlumPerson'},
            'account_name': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'grad_year': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'people.athenaperson': {
            'Meta': {'object_name': 'AthenaPerson'},
            'add_date': ('django.db.models.fields.DateField', [], {}),
            'del_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'krb_name': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'mod_date': ('django.db.models.fields.DateField', [], {}),
            'office_location': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'person_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.PersonType']"}),
            'unit_name': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True'}),
            'year': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'})
        },
        'people.persontype': {
            'Meta': {'object_name': 'PersonType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        }
    }

    complete_apps = ['people']
