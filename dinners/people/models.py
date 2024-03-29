from django.db import models

# Create your models here.

class PersonType(models.Model):
    name            = models.CharField(max_length=60)
    mutable         = models.BooleanField(default=True)
    student         = models.BooleanField(default=False)
    faculty         = models.BooleanField(default=False)

    def __unicode__(self, ):
        return self.name



class AthenaPerson(models.Model):
    krb_name        = models.CharField(max_length=8, verbose_name='Kerberos name', unique=True, )
    person_type     = models.ForeignKey(PersonType)
    office_location = models.CharField(max_length=45,   null=True, blank=True)
    first_name      = models.CharField(max_length=45,   null=True, blank=True)
    year            = models.CharField(max_length=1,    null=True, blank=True)
    unit_name       = models.CharField(max_length=45,   null=True, blank=True)
    last_name       = models.CharField(max_length=45)
    add_date        = models.DateField(help_text="Date when this person was added to the dump.", )
    del_date        = models.DateField(help_text="Date when this person was removed from the dump.", blank=True, null=True, )
    mod_date        = models.DateField(help_text="Date when this person's record was last changed.", blank=True, null=True, )

    def __unicode__(self, ):
        return self.krb_name

    def display_name(self, ):
        return "%s %s" % (self.first_name, self.last_name, )

    def contact_email(self, ):
        return "%s@mit.edu" % (self.krb_name, )


class AlumPerson(models.Model):
    account_name    = models.CharField(max_length=8, unique=True, )
    grad_year       = models.IntegerField()
    first_name      = models.CharField(max_length=30)
    last_name       = models.CharField(max_length=30)

    def __unicode__(self, ):
        return self.account_name

    def display_name(self, ):
        return "%s %s" % (self.first_name, self.last_name, )

    def contact_email(self, ):
        return "%s@alum.mit.edu" % (self.account_name, )
