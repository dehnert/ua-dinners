# Create your views here.
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.urlresolvers import reverse
from django.forms import Form, ModelForm
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, Template
from django.template import RequestContext
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.views.generic import list_detail


import settings
from dinners.core.models import Dinner, DinnerParticipant, DinnerProgram
import dinners.core.models
import dinners.people.forms

def select_program(http_request, forview=None, urlname=None, pagename=None):
    """Allow selecting a program before going to another page.

    Displays all currently enabled programs, and allows the user to select
    one. Upon selection, the user will be forwarded to the URL reverse
    resolution of the URL named ``urlname'' (or ``forview'', if unset).

    The page will be rendered with a pagename of ``pagename'' (or ``forview''
    if unset."""
    if urlname is None:
        urlname = forview
    if pagename is None:
        pagename = forview
    if urlname is None:
        # urlname was None and forview was None
        raise ValueError
    qs = dinners.core.models.DinnerProgram.objects.filter(enabled=True,)
    return list_detail.object_list(
        http_request,
        queryset=qs,
        extra_context={
            'pagename':pagename,
            'urlname': urlname
        },
    )

@user_passes_test(lambda u: u.has_perm('core.view_dinners'))
def view_dinners(http_request, program_slug, ):
    program = get_object_or_404(dinners.core.models.DinnerProgram, slug=program_slug, )
    qs = dinners.core.models.Dinner.objects.filter(program=program,)
    return list_detail.object_list(
        http_request,
        queryset=qs,
        extra_context={
            'pagename':'view_request',
            'program': program,
        },
    )

@user_passes_test(lambda u: u.has_perm('core.view_dinners'))
def view_dinner(http_request, program_slug, dinner_id, ):
    program = get_object_or_404(dinners.core.models.DinnerProgram, slug=program_slug, )
    qs = dinners.core.models.Dinner.objects.filter(program=program,)
    return list_detail.object_detail(
        http_request,
        qs,
        dinner_id,
        extra_context={
            'pagename':'view_request',
            'program': program,
        },
    )

def DinnerFormFactory(program):
    class DinnerForm(Form):
        required_css_class = 'required'
        if program.allow_prof:
            professor = dinners.people.forms.AthenaPerson_ChoiceField_Factory(require_prof=True, )
        if program.allow_alum:
            alum = dinners.people.forms.AlumPerson_ChoiceField_Factory()
    for i in range(0, program.max_students):
        required = (i < program.min_students)
        args = {
            'required':required,
            'label':'Student',
        }
        field = dinners.people.forms.AthenaPerson_ChoiceField_Factory(args, require_student=True, )
        DinnerForm.base_fields['student_'+str(i)] = field
    print "DinnerForm:", DinnerForm.__dict__
    return DinnerForm

@login_required
def register_dinner(http_request, program_slug):
    program = get_object_or_404(DinnerProgram, slug=program_slug)

    context = {
        'program':program,
        'pagename':'register_dinner',
    }

    if not program.enabled:
        return render_to_response('dinners/disabled-program.html', context, context_instance=RequestContext(http_request), )

    initial = {}

    DinnerForm = DinnerFormFactory(program)
    new_dinner = None

    if http_request.method == 'POST': # If the form has been submitted...
        form = DinnerForm(http_request.POST, ) # A form bound to the POST data

        if form.is_valid(): # All validation rules pass
            new_dinner = Dinner()
            new_dinner.creator = http_request.user.username
            new_dinner.program = program
            if 'professor' in form.cleaned_data:
                new_dinner.prof = form.cleaned_data['professor']
            if 'alum' in form.cleaned_data:
                new_dinner.alum = form.cleaned_data['alum']
            new_dinner.save()
            for i in range(0, program.max_students):
                name = "student_" + str(i)
                if form.cleaned_data[name]:
                    print "Found ", name
                    part = form.cleaned_data[name]
                    part_obj = DinnerParticipant(
                        dinner=new_dinner, person=part,
                        confirmed=dinners.core.models.CONFIRM_UNSET,
                        valid=dinners.core.models.VALID_UNSET,
                    )
                    if part.person_type.student:
                        part_obj.valid=dinners.core.models.VALID_AUTOVALIDATED
                    part_obj.save()
            print form.__dict__

            # Send email
            send_register_student_email(http_request.user, program, new_dinner, )
            send_register_guest_email(http_request.user, program, new_dinner, )


            form = None
    else:
        form = DinnerForm(initial=initial, ) # An unbound form

    context['dinner'] = new_dinner
    context['form'] = form

    return render_to_response('dinners/register.html', context, context_instance=RequestContext(http_request), )

def send_register_student_email(creator, program, dinner, ):
    tmpl = get_template('dinners/emails/register_student.txt')
    ctx = Context({
        'creator': creator,
        'program': program,
        'guest': dinner.guest_of_honor_with_title(),
        'confirmlink' : settings.SITE_URL_BASE + reverse('confirm_dinner', kwargs=dict(action='confirm', dinner_id=dinner.pk), ),
        'rejectlink'  : settings.SITE_URL_BASE + reverse('confirm_dinner', kwargs=dict(action='reject', dinner_id=dinner.pk), ),
    })
    body = tmpl.render(ctx)
    to_recipients = [person.contact_email() for person in dinner.get_students()]
    bcc_recipients = [program.archive_addr]
    email = EmailMessage(
        subject='Registered dinner with %s' % (dinner.guest_of_honor_with_title()),
        body=body,
        from_email=program.contact_addr,
        to=to_recipients,
        bcc=bcc_recipients,
    )
    email.send()

def send_register_guest_email(creator, program, dinner, ):
    guest = dinner.guest_of_honor()
    tmpl = get_template('dinners/emails/register_guest.txt')
    ctx = Context({
        'creator': creator,
        'program': program,
        'dinner': dinner,
        'guest': guest,
    })
    print dinner.students.all()
    body = tmpl.render(ctx)
    to_recipients = [guest.contact_email()]
    bcc_recipients = [program.archive_addr]
    email = EmailMessage(
        subject=program.dinner_name,
        body=body,
        from_email=program.contact_addr,
        to=to_recipients,
        bcc=bcc_recipients,
    )
    email.send()


@login_required
def confirm_dinner(http_request, action, dinner_id):
    dinner_id = int(dinner_id)
    print "confirm_dinner", action, dinner_id
    dinner = get_object_or_404(Dinner, pk=dinner_id)

    # Inform user they confirmed
    context = {
        'action':action,
        'dinner':dinner,
        'user':http_request.user,
        'pagename':'confirm_dinner',
    }

    parts = DinnerParticipant.objects.filter(dinner=dinner, person__krb_name=http_request.user.username)
    print "parts", parts
    if len(parts) == 0:
        context['code'] = '404 Page Not Found'
        context['message'] = 'You do not appear to be a participant in this dinner.'
        response = render_to_response('dinners/confirm.not-member.html', context, context_instance=RequestContext(http_request), )
        response.status_code = 404
        return response
    elif len(parts) == 1:
        part = parts[0]
    else:
        context['code'] = '500 Internal Server Error'
        context['message'] = "You appear to be a participant in this dinner multiple times over. This shouldn't happen."
        response = render_to_response('dinners/confirm.multi-member.html', context, context_instance=RequestContext(http_request), )
        response.status_code = 500
        return response
    if action == 'reject':
        part.confirmed = dinners.core.models.CONFIRM_REJECTED
    elif action == 'confirm':
        part.confirmed = dinners.core.models.CONFIRM_CONFIRMED
    else:
        raise Http404
    part.save()

    # Possibly inform attendees that the dinner is schedulable
    blockers = dinner.date_registration_blockers()
    if len(blockers) == 0:
        send_schedulable_email(dinner)

    context['part'] = part

    return render_to_response('dinners/confirm.html', context, context_instance=RequestContext(http_request), )

def send_schedulable_email(dinner):
    program = dinner.program
    guest_name = dinner.guest_of_honor_with_title()
    tmpl = get_template('dinners/emails/schedulable.txt')
    ctx = Context({
        'program': program,
        'dinner': dinner,
        'guest': guest_name,
        'schedulelink' : settings.SITE_URL_BASE + reverse('schedule_dinner', kwargs=dict(dinner_id=dinner.pk), ),
    })
    body = tmpl.render(ctx)
    to_recipients = [part.person.contact_email() for part in dinner.student_attendees()]
    bcc_recipients = [program.archive_addr]
    email = EmailMessage(
        subject='Scheduling dinner with ' + guest_name,
        body=body,
        from_email=program.contact_addr,
        to=to_recipients,
        bcc=bcc_recipients,
    )
    email.send()

class DinnerScheduleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DinnerScheduleForm, self).__init__(*args, **kwargs)
        self.fields['dinner_time'].help_text = "Format: YYYY-MM-DD HH:MM (e.g., 1776-06-04 19:00 for 7PM on the 4th of July)"
    class Meta:
        model = Dinner
        fields = ('dinner_place', 'dinner_time', )

@login_required
def schedule_dinner(http_request, dinner_id, ):
    dinner_id = int(dinner_id)
    dinner = get_object_or_404(Dinner, pk=dinner_id)
    blockers = dinner.date_registration_blockers()
    context = {
        'dinner':   dinner,
        'blockers': blockers,
        'pagename': 'schedule_dinner',
    }
    if len(blockers) > 0:
        context['blockers'] = blockers
        return render_to_response('dinners/schedule_fail.html', context, context_instance=RequestContext(http_request), )
    else:
        form = DinnerScheduleForm(http_request.POST, instance=dinner)
        if http_request.method == 'POST':
            if form.is_valid():
                form.save()
                send_scheduled_email(dinner)
                return render_to_response('dinners/schedule_success.html', context, context_instance=RequestContext(http_request), )
        context['form'] = form
        return render_to_response('dinners/schedule.html', context, context_instance=RequestContext(http_request), )

def send_scheduled_email(dinner):
    program = dinner.program
    guest_name = dinner.guest_of_honor_with_title()
    students = [part.person for part in dinner.student_attendees()]
    tmpl = get_template('dinners/emails/scheduled.txt')
    ctx = Context({
        'program': program,
        'dinner': dinner,
        'guest_name': guest_name,
        'students': students,
        'amount': (len(students)+1)*program.person_money_cap,
    })
    body = tmpl.render(ctx)
    to_recipients = [person.contact_email() for person in students]
    bcc_recipients = [program.archive_addr]
    email = EmailMessage(
        subject='Dinner with %s --- REIMBURSEMENT INSTRUCTIONS' % (guest_name,),
        body=body,
        from_email=program.contact_addr,
        to=to_recipients,
        bcc=bcc_recipients,
    )
    email.send()
