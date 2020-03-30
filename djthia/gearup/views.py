# -*- coding: utf-8 -*-

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from djimix.decorators.auth import portal_auth_required
from djtools.utils.mail import send_mail
from djthia.gearup.forms import QuestionnaireForm


REQ_ATTR = settings.REQUIRED_ATTRIBUTE


@portal_auth_required(
    session_var='DJTHIA_AUTH',
    redirect_url=reverse_lazy('access_denied'),
)
def donation(request, pid=None):
    """Donation form."""
    return render(request, 'gearup/donation.html', {})


@portal_auth_required(
    session_var='DJTHIA_AUTH',
    redirect_url=reverse_lazy('access_denied'),
)
def notes(request, pid=None):
    """Notes form."""
    return render(request, 'gearup/notes.html', {})


@portal_auth_required(
    session_var='DJTHIA_AUTH',
    redirect_url=reverse_lazy('access_denied'),
)
def questionnaire(request):
    """Questionnaire form."""
    if settings.DEBUG:
        to_list = [settings.SERVER_EMAIL]
    else:
        to_list = [settings.GEARUP_EMAIL]

    if request.method == 'POST':
        form = QuestionnaireForm(
            request.POST, request.FILES, use_required_attribute=REQ_ATTR,
        )
        if form.is_valid():
            grad = form.save()
            email = settings.DEFAULT_FROM_EMAIL
            if grad.email:
                email = grad.email
            subject = "[Submit] {0} {1}".format(grad.first_name, grad.last_name)
            send_mail(
                request, to_list, subject, email, 'gearup/email.html', grad,
            )
            return HttpResponseRedirect(reverse_lazy('gearup_success'))
    else:
        form = QuestionnaireForm(use_required_attribute=REQ_ATTR)
    return render(request, 'gearup/form.html', {'form': form})
