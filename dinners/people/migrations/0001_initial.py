
from south.db import db
from django.db import models
from people.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'AthenaPerson'
        db.create_table('people_athenaperson', (
            ('id', orm['people.AthenaPerson:id']),
            ('krb_name', orm['people.AthenaPerson:krb_name']),
            ('person_type', orm['people.AthenaPerson:person_type']),
            ('office_location', orm['people.AthenaPerson:office_location']),
            ('first_name', orm['people.AthenaPerson:first_name']),
            ('year', orm['people.AthenaPerson:year']),
            ('unit_name', orm['people.AthenaPerson:unit_name']),
            ('last_name', orm['people.AthenaPerson:last_name']),
            ('add_date', orm['people.AthenaPerson:add_date']),
            ('del_date', orm['people.AthenaPerson:del_date']),
            ('mod_date', orm['people.AthenaPerson:mod_date']),
        ))
        db.send_create_signal('people', ['AthenaPerson'])
        
        # Adding model 'AlumPerson'
        db.create_table('people_alumperson', (
            ('id', orm['people.AlumPerson:id']),
            ('account_name', orm['people.AlumPerson:account_name']),
            ('grad_year', orm['people.AlumPerson:grad_year']),
        ))
        db.send_create_signal('people', ['AlumPerson'])
        
        # Adding model 'PersonType'
        db.create_table('people_persontype', (
            ('id', orm['people.PersonType:id']),
            ('name', orm['people.PersonType:name']),
        ))
        db.send_create_signal('people', ['PersonType'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'AthenaPerson'
        db.delete_table('people_athenaperson')
        
        # Deleting model 'AlumPerson'
        db.delete_table('people_alumperson')
        
        # Deleting model 'PersonType'
        db.delete_table('people_persontype')
        
    
    
    models = {
        'people.alumperson': {
            'account_name': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'grad_year': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'people.athenaperson': {
            'add_date': ('django.db.models.fields.DateField', [], {}),
            'del_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'krb_name': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'mod_date': ('django.db.models.fields.DateField', [], {}),
            'office_location': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'person_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.PersonType']"}),
            'unit_name': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'year': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'people.persontype': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        }
    }
    
    complete_apps = ['people']
