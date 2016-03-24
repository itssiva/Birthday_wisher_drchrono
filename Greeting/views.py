from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from .forms import GreetingForm
from .models import Greetings


patient_attributes = ['<patient_first_name>', '<patient_last_name>', '<patient_age>']
doctors_attributes = ['<doctor_first_name>', '<doctor_last_name>', '<doctor_email>', '<doctor_specialty>',
                      '<doctor_job_title>', '<doctor_suffix>', '<doctor_website>', '<doctor_home_phone>',
                      '<doctor_office_phone>', '<doctor_cell_phone>'
                     ]

def home(request):
    data = {}
    if request.user.is_authenticated():
        try:
            greeting = Greetings.objects.get(user=request.user)
        except Greetings.DoesNotExist:
            raise Http404

        data = {
            'type': greeting.greeting_type,
            'is_active': greeting.is_active
        }
    return render_to_response('home.html', data, RequestContext(request))


@login_required
def customize_greeting(request):
    """
    customizes the default content with the user preferred content
    """
    user = request.user
    greeting = Greetings.objects.get(user=user)
    form = GreetingForm()
    if request.POST:
        form = GreetingForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            greeting_type = data['greeting_type']
            if greeting_type == 'e':
                greeting.email_subject = data['email_subject']
                greeting.email_body = data['email_body']
            else:
                greeting.sms_message = data['sms_message']
                greeting.sms_signature = data['sms_signature']
            greeting.save()
            return HttpResponseRedirect(reverse('home'))

    return render_to_response('customize.html',
                                  {
                                      'form': form,
                                      'greeting': greeting,
                                      'patient_attributes': patient_attributes,
                                      'doctor_attributes': doctors_attributes,
                                  }, RequestContext(request))


def activate(request):
    """
    toggles the activation and deactivation of the service for the user
    """
    greeting = Greetings.objects.get(user=request.user)
    is_active = greeting.is_active
    if is_active is True:
        is_active = False
    else:
        is_active = True
    greeting.is_active = is_active
    greeting.save()
    return HttpResponseRedirect(reverse('home'))


def change_greeting_type(request):
    """
    toggles the greeting type of the user between email and SMS
    """
    greeting = Greetings.objects.get(user=request.user)
    state = greeting.greeting_type
    if state == 'e':
        state = 's'
    else:
        state = 'e'
    greeting.greeting_type = state
    greeting.save()
    return HttpResponseRedirect(reverse('home'))
