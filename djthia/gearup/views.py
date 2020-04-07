# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from djauth.LDAPManager import LDAPManager
from djimix.decorators.auth import portal_auth_required
from djthia.core.decorators import eligibility
from djthia.core.utils import get_student
from djthia.gearup.forms import AnnotationForm
from djthia.gearup.forms import CapGownForm
from djthia.gearup.forms import DocumentForm
from djthia.gearup.forms import PhoneticForm
from djthia.gearup.forms import QuestionnaireForm
from djtools.utils.mail import send_mail


REQ_ATTR = settings.REQUIRED_ATTRIBUTE


@portal_auth_required(
    session_var='DJTHIA_AUTH',
    redirect_url=reverse_lazy('access_denied'),
)
@eligibility
def donation(request):
    """Donation form."""
    return render(request, 'gearup/donation.html', {})


@portal_auth_required(
    session_var='DJTHIA_AUTH',
    redirect_url=reverse_lazy('access_denied'),
)
@eligibility
def counseling(request):
    """Exit counseling document upload form."""
    user = request.user
    try:
        questionnaire = user.questionnaire
    except Exception:
        questionnaire = None
    if questionnaire:
        if request.method == 'POST':
            form = DocumentForm(
                request.POST, request.FILES, use_required_attribute=REQ_ATTR,
            )
            if form.is_valid():
                doc = form.save(commit=False)
                doc.questionnaire = user.questionnaire
                doc.created_by = user
                doc.updated_by = user
                doc.save()
                doc.tags.add('Finaid')
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    "Document saved",
                    extra_tags='alert-success',
                )
                frum = user.email
                if doc.questionnaire.email:
                    frum = doc.questionnaire.email
                subject = "[Exit Counseling Form] {0} {1}".format(
                    user.first_name, user.last_name,
                )
                send_mail(
                    request,
                    [settings.EXIT_COUNSELING_EMAIL],
                    subject,
                    frum,
                    'gearup/counseling_email.html',
                    doc,
                )
                return HttpResponseRedirect(reverse_lazy('home'))
        else:
            form = DocumentForm(use_required_attribute=REQ_ATTR)
    else:
        messages.add_message(
            request,
            messages.WARNING,
            "Please submit the Gear Up questionnaire",
            extra_tags='alert-warning',
        )
        return HttpResponseRedirect(reverse_lazy('home'))
    return render(
        request, 'gearup/counseling.html', {'form': form},
    )


@portal_auth_required(
    session_var='DJTHIA_AUTH',
    redirect_url=reverse_lazy('access_denied'),
)
@eligibility
def capgown(request):
    """Cap and gown form."""
    user = request.user
    try:
        questionnaire = user.questionnaire
    except Exception:
        questionnaire = None
    if questionnaire:
        if request.method == 'POST':
            form = CapGownForm(
                request.POST,
                instance=questionnaire,
                use_required_attribute=REQ_ATTR,
            )
            if form.is_valid():
                cap = form.save(commit=False)
                cap.updated_by = user
                cap.save()
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    "Cap and Gown form saved",
                    extra_tags='alert-success',
                )
                return HttpResponseRedirect(reverse_lazy('home'))
        else:
            form = CapGownForm(
                use_required_attribute=REQ_ATTR,
                instance=questionnaire,
            )
    else:
        messages.add_message(
            request,
            messages.WARNING,
            "Please submit the Gear Up questionnaire",
            extra_tags='alert-warning',
        )
        return HttpResponseRedirect(reverse_lazy('home'))
    return render(
        request, 'gearup/capgown.html', {
            'form': form, 'questionnaire': questionnaire,
        },
    )


@portal_auth_required(
    session_var='DJTHIA_AUTH',
    redirect_url=reverse_lazy('access_denied'),
)
@eligibility
def notes(request):
    """Notes form."""
    user = request.user
    try:
        questionnaire = user.questionnaire
    except Exception:
        questionnaire = None
    if questionnaire:
        if request.method == 'POST':
            form = AnnotationForm(request.POST, use_required_attribute=REQ_ATTR)
            if form.is_valid():
                form_data = form.cleaned_data
                note = form.save(commit=False)
                note.questionnaire = user.questionnaire
                note.created_by = user
                note.updated_by = user
                note.save()
                cid = form_data['recipients']
                try:
                    recipient = User.objects.get(pk=cid)
                except Exception:
                    lman = LDAPManager()
                    luser = lman.search(cid)
                    recipient = lman.dj_create(luser)
                note.recipients.add(recipient)

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
    try:
        gearup = user.questionnaire
    except Exception:
        gearup = None
    if gearup:
        messages.add_message(
            request,
            messages.WARNING,
            "You have already submitted the Gear Up questionnaire.",
            extra_tags='alert-warning',
        )
        return HttpResponseRedirect(reverse_lazy('home'))
    else:
        # fetch student data
        student = get_student(user.id)
        if request.method == 'POST':
            form = QuestionnaireForm(
                request.POST, use_required_attribute=REQ_ATTR,
            )
            pho_form = PhoneticForm(
                request.POST, request.FILES, use_required_attribute=REQ_ATTR,
            )
            if form.is_valid() and pho_form.is_valid():
                grad = form.save(commit=False)
                grad.created_by = user
                grad.updated_by = user
                grad.save()
                # audio file
                doc = pho_form.save(commit=False)
                doc.questionnaire = grad
                doc.created_by = user
                doc.updated_by = user
                doc.save()
                doc.tags.add('Phonetics')
                return HttpResponseRedirect(reverse_lazy('gearup_success'))
        else:
            form = QuestionnaireForm(use_required_attribute=REQ_ATTR)
            pho_form = PhoneticForm(use_required_attribute=REQ_ATTR)
        return render(
            request,
            'gearup/questionnaire.html',
            {'form': form, 'pho_form': pho_form, 'student': student},
        )
