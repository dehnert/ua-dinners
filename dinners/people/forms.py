# Custom form types for People
from django.forms.models import ModelChoiceField
from django.forms.widgets import TextInput

import people.models

def AthenaPerson_ChoiceField_Factory(field_args=None):
    if field_args is None: field_args = {}
    return ModelChoiceField(
        widget=TextInput(attrs={'maxlength':8}),
        to_field_name='krb_name',
        queryset=people.models.AthenaPerson.objects.all(),
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

