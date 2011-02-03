from dinners.core.models import DinnerProgram, Dinner, DinnerParticipant
from django.contrib import admin


class DinnerParticipantInline(admin.TabularInline):
    model = DinnerParticipant
    raw_id_fields = ('person', )
    extra = 5

def copy_programs(modeladmin, request, queryset):
    for program in queryset:
        program.copy()

class DinnerProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'enabled', 'min_students', 'max_students', 'person_money_cap', 'allow_alum', 'allow_prof', 'dinner_name', 'sponsor_long', )
    list_display_links = ('slug', 'name', )
    actions = [copy_programs]

class DinnerAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Request Basics', {'fields': ['program', 'creator' , 'create_time', ] }),
        ('Details', {'fields': ['dinner_place', 'dinner_time', ] }),
        ('Guests of Honor', {'fields': ['prof', 'alum', ] }),
    ]
    inlines = ( DinnerParticipantInline, )

    list_display = ('id', 'program', 'creator', 'prof', 'alum', )
    list_display_links = ('id', 'program', 'creator', )

    raw_id_fields = ('prof', 'alum', )

admin.site.register(DinnerProgram, DinnerProgramAdmin)
admin.site.register(Dinner, DinnerAdmin)
