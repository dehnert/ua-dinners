
from south.db import db
from django.db import models
from dinners.core.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'DinnerProgram.archive_addr'
        archive = orm['core.dinnerprogram:archive_addr']
        archive.default = 'ua-dinners-dev@mit.edu'
        db.add_column('core_dinnerprogram', 'archive_addr', archive, keep_default=False)
        
        # Adding field 'DinnerProgram.contact_addr'
        contact = orm['core.dinnerprogram:contact_addr']
        contact.default = 'ua-dinners-dev@mit.edu'
        db.add_column('core_dinnerprogram', 'contact_addr', contact, keep_default=False)
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'DinnerProgram.archive_addr'
        db.delete_column('core_dinnerprogram', 'archive_addr')
        
        # Deleting field 'DinnerProgram.contact_addr'
        db.delete_column('core_dinnerprogram', 'contact_addr')
        
    
    
    models = {
        'core.dinner': {
            'alum': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'prof_dinners'", 'null': 'True', 'to': "orm['people.AlumPerson']"}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'creator': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'dinner_place': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'dinner_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'prof': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.AthenaPerson']", 'null': 'True', 'blank': 'True'}),
            'program': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.DinnerProgram']"}),
            'students': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['people.AthenaPerson']"})
        },
        'core.dinnerparticipant': {
            'confirmed': ('django.db.models.fields.IntegerField', [], {}),
            'dinner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Dinner']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.AthenaPerson']"}),
            'valid': ('django.db.models.fields.IntegerField', [], {})
        },
        'core.dinnerprogram': {
            'allow_alum': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'allow_prof': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'archive_addr': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'contact_addr': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_students': ('django.db.models.fields.IntegerField', [], {}),
            'min_students': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'person_money_cap': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'total_money_cap': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'})
        },
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
    
    complete_apps = ['core']
