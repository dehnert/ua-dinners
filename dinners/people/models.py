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

