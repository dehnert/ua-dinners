from django.db import models

# Create your models here.

class PersonType(models.Model):
    name            = models.CharField(max_length=60)


class AthenaPerson(models.Model):
    person_type     = models.ForeignKey(PersonType)
    office_location = models.CharField(max_length=30)
    first_name      = models.CharField(max_length=30)
    year            = models.CharField(max_length=1)
    unit_name       = models.CharField(max_length=16)
    last_name       = models.CharField(max_length=30)
    krb_name        = models.CharField(max_length=8)
    add_date        = models.DateField(help_text="Date when this person was added to the dump.")
    del_date        = models.DateField(help_text="Date when this person was removed from the dump.")
    mod_date        = models.DateField(help_text="Date when this person's record was last changed.")


class AlumPerson(models.Model):
    account_name    = models.CharField(max_length=8)
    grad_year       = models.IntegerField()
