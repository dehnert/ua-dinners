# Create your views here.
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.urlresolvers import reverse
from django.forms import Form, ModelForm
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext


from dinners.core.models import Dinner, DinnerParticipant, DinnerProgram
import dinners.core.models
import dinners.people.forms

def DinnerFormFactory(program):
    class DinnerForm(Form):
        required_css_class = 'required'
        if program.allow_prof:
            professor = dinners.people.forms.AthenaPerson_ChoiceField_Factory()
        if program.allow_alum:
            alum = dinners.people.forms.AlumPerson_ChoiceField_Factory()
    for i in range(0, program.max_students):
        required = (i < program.min_students)
        args = {
            'required':required,
            'label':'Student',
        }
        field = dinners.people.forms.AthenaPerson_ChoiceField_Factory(args)
        DinnerForm.base_fields['student_'+str(i)] = field
    print "DinnerForm:", DinnerForm.__dict__
    return DinnerForm

def select_program(http_request):
    pass

@login_required
def register_dinner(http_request, program_slug):
    program = get_object_or_404(DinnerProgram, slug=program_slug)

    initial = {}

    DinnerForm = DinnerFormFactory(program)
    new_dinner = None

    if http_request.method == 'POST': # If the form has been submitted...
        form = DinnerForm(http_request.POST, ) # A form bound to the POST data

        if form.is_valid(): # All validation rules pass
            new_dinner = Dinner()
            new_dinner.creator = http_request.user.username
            new_dinner.program = program
            new_dinner.prof = form.cleaned_data['professor']
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
                    part_obj.save()
            print form.__dict__

            # Send email
            #tmpl = get_template('vouchers/emails/request_submit_admin.txt')
            #ctx = Context({
            #    'submitter': http_request.user,
            #    'request': request_obj,
            #})
            #body = tmpl.render(ctx)
            #recipients = []
            #for name, addr in settings.ADMINS:
            #    recipients.append(addr)
            #recipients.append(request_obj.budget_area.owner_address())
            #if settings.CC_SUBMITTER:
            #    recipients.append(http_request.user.email)
            #send_mail(
            #    '%sRequest submittal: %s requested $%s' % (
            #        settings.EMAIL_SUBJECT_PREFIX,
            #        http_request.user,
            #        request_obj.amount,
            #    ),
            #    body,
            #    settings.SERVER_EMAIL,
            #    recipients,
            #)

            form = None
    else:
        form = DinnerForm(initial=initial, ) # An unbound form

    context = {
        'form':form,
        'dinner':new_dinner,
        'program':program,
        'pagename':'register_dinner',
    }
    return render_to_response('dinners/register.html', context, context_instance=RequestContext(http_request), )
 
