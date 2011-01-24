# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'DinnerProgram.dinners_deadline'
        db.add_column('core_dinnerprogram', 'dinners_deadline', self.gf('django.db.models.fields.DateField')(default=datetime.date(2011, 1, 23)), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'DinnerProgram.dinners_deadline'
        db.delete_column('core_dinnerprogram', 'dinners_deadline')


    models = {
        'core.dinner': {
            'Meta': {'object_name': 'Dinner'},
            'alum': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'prof_dinners'", 'null': 'True', 'to': "orm['people.AlumPerson']"}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'creator': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'dinner_place': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'dinner_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'prof': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.AthenaPerson']", 'null': 'True', 'blank': 'True'}),
            'program': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.DinnerProgram']"}),
            'students': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'student_dinners'", 'symmetrical': 'False', 'through': "orm['core.DinnerParticipant']", 'to': "orm['people.AthenaPerson']"})
        },
        'core.dinnerparticipant': {
            'Meta': {'object_name': 'DinnerParticipant'},
            'confirmed': ('django.db.models.fields.IntegerField', [], {}),
            'dinner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Dinner']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.AthenaPerson']"}),
            'valid': ('django.db.models.fields.IntegerField', [], {})
        },
        'core.dinnerprogram': {
            'Meta': {'object_name': 'DinnerProgram'},
            'allow_alum': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'allow_prof': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'archive_addr': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'contact_addr': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'dinners_deadline': ('django.db.models.fields.DateField', [], {}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_students': ('django.db.models.fields.IntegerField', [], {}),
            'min_students': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'person_money_cap': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'total_money_cap': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'})
        },
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
            'office_location': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'person_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.PersonType']"}),
            'unit_name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'year': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'people.persontype': {
            'Meta': {'object_name': 'PersonType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        }
    }

    complete_apps = ['core']
