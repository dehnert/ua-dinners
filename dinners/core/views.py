# Create your views here.
from django.contrib.auth.decorators import user_passes_test, login_required
from django.forms import ModelForm
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext


from dinners.core.models import Dinner, DinnerProgram

class DinnerForm(ModelForm):
    class Meta:
        model = Dinner


def select_program(http_request):
    pass

def register_dinner(http_request, program_slug):
    program = get_object_or_404(DinnerProgram, slug=program_slug)

    new_dinner = Dinner()
    new_dinner.creator = http_request.user.username
    new_dinner.program = program

    # Prefill from user information (itself prefilled from LDAP now)
    initial = {}

    if http_request.method == 'POST': # If the form has been submitted...
        form = DinnerForm(http_request.POST, instance=new_dinner) # A form bound to the POST data

        if form.is_valid(): # All validation rules pass
            dinner_obj = form.save()
            print "save result:", dinner_obj.__dict__
            print "orig obj:   ", new_dinner.__dict__

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

            #return HttpResponseRedirect(reverse(review_request, args=[new_dinner.pk],) + '?new=true') # Redirect after POST
    else:
        form = DinnerForm(instance=new_dinner, initial=initial, ) # An unbound form

    context = {
        'form':form,
        'program':program,
        'pagename':'register_dinner',
    }
    return render_to_response('dinners/register.html', context, context_instance=RequestContext(http_request), )
 
