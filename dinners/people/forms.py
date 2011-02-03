# Custom form types for People
from django.core.exceptions import ValidationError
from django.forms.models import ModelChoiceField
from django.forms.widgets import TextInput

import people.models

def require_student_validator(person):
    if person.person_type.student:
        pass
    else:
        raise ValidationError(u'%s is not a student.' % (person, ))

def require_prof_validator(person):
    if person.person_type.faculty:
        pass
    else:
        raise ValidationError(u'%s is not a faculty member.' % (person, ))

def AthenaPerson_ChoiceField_Factory(field_args=None,
    require_student=False, require_prof=False, ):
    if field_args is None: field_args = {}
    validators = []
    if require_student: validators.append(require_student_validator)
    if require_prof: validators.append(require_prof_validator)
    return ModelChoiceField(
        widget=TextInput(attrs={'maxlength':8}),
        to_field_name='krb_name',
        queryset=people.models.AthenaPerson.objects.all(),
        validators=validators,
        **field_args
    )

def AlumPerson_ChoiceField_Factory(field_args=None):
    if field_args is None: field_args = {}
    return ModelChoiceField(
        widget=TextInput(attrs={'maxlength':8}),
        to_field_name='account_name',
        queryset=people.models.AlumPerson.objects.all(),
        **field_args
    )

