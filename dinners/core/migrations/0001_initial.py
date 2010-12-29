
from south.db import db
from django.db import models
from dinners.core.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'DinnerProgram'
        db.create_table('core_dinnerprogram', (
            ('id', orm['core.DinnerProgram:id']),
            ('slug', orm['core.DinnerProgram:slug']),
            ('name', orm['core.DinnerProgram:name']),
            ('enabled', orm['core.DinnerProgram:enabled']),
            ('min_students', orm['core.DinnerProgram:min_students']),
            ('max_students', orm['core.DinnerProgram:max_students']),
            ('person_money_cap', orm['core.DinnerProgram:person_money_cap']),
            ('total_money_cap', orm['core.DinnerProgram:total_money_cap']),
            ('allow_alum', orm['core.DinnerProgram:allow_alum']),
            ('allow_prof', orm['core.DinnerProgram:allow_prof']),
        ))
        db.send_create_signal('core', ['DinnerProgram'])
        
        # Adding model 'DinnerParticipant'
        db.create_table('core_dinnerparticipant', (
            ('id', orm['core.DinnerParticipant:id']),
            ('dinner', orm['core.DinnerParticipant:dinner']),
            ('person', orm['core.DinnerParticipant:person']),
            ('confirmed', orm['core.DinnerParticipant:confirmed']),
            ('valid', orm['core.DinnerParticipant:valid']),
        ))
        db.send_create_signal('core', ['DinnerParticipant'])
        
        # Adding model 'Dinner'
        db.create_table('core_dinner', (
            ('id', orm['core.Dinner:id']),
            ('program', orm['core.Dinner:program']),
            ('prof', orm['core.Dinner:prof']),
            ('alum', orm['core.Dinner:alum']),
            ('creator', orm['core.Dinner:creator']),
            ('create_time', orm['core.Dinner:create_time']),
            ('dinner_place', orm['core.Dinner:dinner_place']),
            ('dinner_time', orm['core.Dinner:dinner_time']),
        ))
        db.send_create_signal('core', ['Dinner'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'DinnerProgram'
        db.delete_table('core_dinnerprogram')
        
        # Deleting model 'DinnerParticipant'
        db.delete_table('core_dinnerparticipant')
        
        # Deleting model 'Dinner'
        db.delete_table('core_dinner')
        
    
    
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
