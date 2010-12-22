from dinners.core.models import DinnerProgram, Dinner, DinnerParticipant
from django.contrib import admin


class DinnerParticipantInline(admin.TabularInline):
    model = DinnerParticipant
    extra = 5

class DinnerProgramAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'enabled', 'min_students', 'max_students', 'person_money_cap', 'allow_alum', 'allow_prof', )
    list_display_links = ('slug', 'name', )

class DinnerAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Request Basics', {'fields': ['program', 'creator' , 'create_time', ] }),
        ('Details', {'fields': ['dinner_place', 'dinner_time', ] }),
        ('Guests of Honor', {'fields': ['prof', 'alum', ] }),
    ]
    inlines = ( DinnerParticipantInline, )

    list_display = ('id', 'program', 'creator', 'prof', 'alum', )
    list_display_links = ('id', 'program', 'creator', )

admin.site.register(DinnerProgram, DinnerProgramAdmin)
admin.site.register(Dinner, DinnerAdmin)
