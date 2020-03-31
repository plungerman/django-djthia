# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from djimix.decorators.auth import portal_auth_required
from djtools.utils.mail import send_mail
from djthia.gearup.forms import AnnotationForm
from djthia.gearup.forms import QuestionnaireForm
from djthia.gearup.models import Questionnaire
from djthia.core.utils import get_student
from djthia.core.decorators import eligibility


REQ_ATTR = settings.REQUIRED_ATTRIBUTE


@portal_auth_required(
    session_var='DJTHIA_AUTH',
    redirect_url=reverse_lazy('access_denied'),
)
@eligibility
def donation(request, pid=None):
    """Donation form."""
    return render(request, 'gearup/donation.html', {})


@portal_auth_required(
    session_var='DJTHIA_AUTH',
    redirect_url=reverse_lazy('access_denied'),
)
@eligibility
def notes(request, pid=None):
    """Notes form."""
    user = request.user
    if user.questionnaire:
        if request.method == 'POST':
            form = AnnotationForm(request.POST, use_required_attribute=REQ_ATTR)
            if form.is_valid():
                note = form.save(commit=False)
                note.questionnaire = user.questionnaire
                note.created_by = user
                note.updated_by = user
                note.save()
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    "Note saved. Submit another?",
                    extra_tags='alert-success',
                )
                return HttpResponseRedirect(reverse_lazy('notes'))
        else:
            form = AnnotationForm(use_required_attribute=REQ_ATTR)
    else:
        messages.add_message(
            request,
            messages.WARNING,
            "Please submit the Gear Up questionnaire",
            extra_tags='alert-warning',
        )
        return HttpResponseRedirect(reverse_lazy('home'))
    return render(
        request, 'gearup/notes.html', {'form': form, 'notes': notes},
    )


@portal_auth_required(
    session_var='DJTHIA_AUTH',
    redirect_url=reverse_lazy('access_denied'),
)
@eligibility
def questionnaire(request):
    """Questionnaire form."""
    user = request.user
    if user.questionnaire:
        messages.add_message(
            request,
            messages.WARNING,
            "You have already submitted the Gear Up questionnaire.",
            extra_tags='alert-warning',
        )
        return HttpResponseRedirect(reverse_lazy('home'))
    else:
        if settings.DEBUG:
            to_list = [settings.SERVER_EMAIL]
        else:
            to_list = [settings.GEARUP_EMAIL]
        # fetch student data
        student = get_student(user.id)
        if request.method == 'POST':
            form = QuestionnaireForm(
                request.POST, request.FILES, use_required_attribute=REQ_ATTR,
            )
            if form.is_valid():
                grad = form.save(commit=False)
                grad.created_by = user
                grad.updated_by = user
                grad.save()
                email = settings.DEFAULT_FROM_EMAIL
                if grad.email:
                    email = grad.email
                subject = "[Submit] {0} {1}".format(
                    user.first_name, user.last_name,
                )
                send_mail(
                    request, to_list, subject, email, 'gearup/email.html', grad,
                )
                return HttpResponseRedirect(reverse_lazy('gearup_success'))
        else:
            form = QuestionnaireForm(use_required_attribute=REQ_ATTR)
        return render(
            request, 'gearup/form.html', {'form': form, 'student': student},
        )
