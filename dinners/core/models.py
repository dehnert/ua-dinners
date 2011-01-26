from django.db import models

import copy
import datetime


TIME_DUEDATE = datetime.timedelta(weeks=3)

# Choices for fields
CONFIRM_UNSET       = 0
CONFIRM_CONFIRMED   = 10
CONFIRM_OVERRIDDEN  = 20    # confirmed by an admin
CONFIRM_REJECTED    = -10   # rejected by the user
CONFIRM_CHOICES = (
    (CONFIRM_UNSET,     "unconfirmed"),
    (CONFIRM_CONFIRMED, "confirmed"),
    (CONFIRM_OVERRIDDEN,"overridden"),
    (CONFIRM_REJECTED,  "rejected"),
)

VALID_UNSET         = 0
VALID_AUTOVALIDATED = 10
VALID_OVERRIDDEN    = 20    # confirmed by an admin
VALID_REJECTED      = -10   # verified by an admin as invalid
VALID_CHOICES = (
    (VALID_UNSET,           "unvalidated"),
    (VALID_AUTOVALIDATED,   "autovalidated"),
    (VALID_OVERRIDDEN,      "hand-validated"),
    (VALID_REJECTED,        "rejected"),
)

# Models themselves
class DinnerProgram(models.Model):
    slug                = models.SlugField(unique=True, )
    name                = models.CharField(max_length=20)
    enabled             = models.BooleanField(help_text="Whether this program is enabled. Set to false to disable new signups for the program.")
    min_students        = models.IntegerField()
    max_students        = models.IntegerField()
    person_money_cap    = models.DecimalField(verbose_name="per-person cap for money", help_text="Maximum amount that a single person (student, faculty, or alum) can be reimbursed for", max_digits=5, decimal_places=2)
    total_money_cap     = models.DecimalField(verbose_name="money cap for entire program", help_text="Maximum amount that the entire program can spend on dinners", max_digits=7, decimal_places=2)
    allow_alum          = models.BooleanField(help_text="Check to allow an alum to be the focus of the dinners.")
    allow_prof          = models.BooleanField(help_text="Check to allow a professor to be the focus of the dinners.")
    contact_addr        = models.EmailField(help_text="Contact address for the program. This address will be used for sending out emails.")
    archive_addr        = models.EmailField(help_text="Archive address for the program. This address will be BCC'd on outgoing emails.")
    dinners_deadline    = models.DateField(help_text="Last date when dinners may take place.")
    dinner_name         = models.CharField(max_length=40, help_text='Name of a dinner --- for example, "Student-Faculty Dinner".')
    sponsor_long        = models.CharField(max_length=40, help_text='Full name of the program sponsor --- for example, "Student Committee on Educational Policy".')
    purpose             = models.TextField(help_text='Put in some nice blurb about why the program exists.')

    def copy(self, ):
        """Copy a DinnerProgram

        Note that if DinnerProgram ever acquires a foreign key or the
        like, the referenced object should probably be copies as well.

        The copy will be saved and returned. If you want to modify it
        further, you can do so. However, you can also completely ignore
        the return value, and it will already have been saved to the DB.
        """
        new_obj = copy.deepcopy(self, )
        new_obj.pk = None
        new_obj.slug = self.slug + "-copy"
        new_obj.name = self.name + " (copy)"
        new_obj.save()
        return new_obj

    def __unicode__(self, ):
        return self.name


class Dinner(models.Model):
    program     = models.ForeignKey(DinnerProgram)
    prof        = models.ForeignKey('people.AthenaPerson', blank=True, null=True, to_field='krb_name', related_name="prof_dinners")
    alum        = models.ForeignKey('people.AlumPerson',   blank=True, null=True, to_field='account_name')
    students    = models.ManyToManyField('people.AthenaPerson', through='DinnerParticipant', related_name="student_dinners")
    creator     = models.CharField(max_length=10)
    create_time = models.DateTimeField(default=datetime.datetime.now)
    dinner_place= models.CharField(max_length=100, blank=True, )
    dinner_time = models.DateTimeField(null=True, blank=True, )

    def get_students(self, ):
        # XXX: students.all doesn't work
        # http://code.djangoproject.com/ticket/15161
        parts = self.students_state().select_related(depth=1)
        return [part.person for part in parts]

    def students_state(self, ):
        return DinnerParticipant.objects.filter(dinner=self,)

    def date_registration_blockers(self, ):
        """Determine who prevents this dinner from being registered.

        In particular, to register a date, the dinner must have no participants
        who are unconfirmed and not invald.
        """
        return self.students_state().filter(confirmed=CONFIRM_UNSET, valid__gte=VALID_UNSET)


    def student_attendees(self, ):
        """
        Return attendees of the dinner.

        This is defined as people who are confirmed and valid.
        """

        parts = self.students_state().filter(
            confirmed__gt=CONFIRM_UNSET,
            valid__gt=VALID_UNSET,
        )
        print "attendees", parts
        return parts

    def guest_of_honor(self, ):
        if self.prof: return self.prof
        if self.alum: return self.alum
        return None

    def guest_of_honor_with_title(self, ):
        guests = []
        if self.prof: guests.append("Professor %s" % (self.prof.display_name()))
        if self.alum: guests.append("alumnus %s" % (self.alum.display_name()))
        if len(guests) == 0:
            raise ValueError, "no guest of honor"
        return " and ".join(guests)

    def schedule_deadline(self, ):
        print "schedule_deadline", self.create_time, (self.create_time + TIME_DUEDATE)
        return self.create_time + TIME_DUEDATE

    def __unicode__(self, ):
        return "Dinner: %s (creator) with %s (guest)" % (self.creator, str(self.guest_of_honor()), )


class DinnerParticipant(models.Model):
    dinner      = models.ForeignKey(Dinner)
    person      = models.ForeignKey("people.AthenaPerson", to_field='krb_name')
    confirmed   = models.IntegerField(choices=CONFIRM_CHOICES)
    valid       = models.IntegerField(choices=VALID_CHOICES)

    def get_confirmed_class(self, ):
        """Get a CSS class for displaying the confirmation state."""
        return "confirmed-" + self.get_confirmed_display()
    def get_valid_class(self, ):
        """Get a CSS class for displaying the confirmation state."""
        return "validated-" + self.get_valid_display()

    def __unicode__(self, ):
        return "%s on [%s] (%s)" % (self.person, self.dinner, self.get_confirmed_display(), )
