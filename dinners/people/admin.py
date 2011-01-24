from people.models import PersonType, AthenaPerson, AlumPerson
from django.contrib import admin


class PersonTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'mutable', 'student', 'faculty', )


class AthenaPersonAdmin(admin.ModelAdmin):
    list_display = ('krb_name', 'person_type', 'first_name', 'last_name', 'year', 'unit_name', 'add_date', 'mod_date', 'del_date', )

admin.site.register(PersonType, PersonTypeAdmin)
admin.site.register(AthenaPerson, AthenaPersonAdmin)
admin.site.register(AlumPerson)
