# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from djauth.managers import LDAPManager
from djauth.decorators import portal_auth_required
from djthia.core.decorators import eligibility
from djthia.core.utils import get_student
from djthia.gearup.forms import AnnotationForm
from djthia.gearup.forms import CapGownForm
from djthia.gearup.forms import CounselingForm
from djthia.gearup.forms import PhoneticForm
from djthia.gearup.forms import PhotoForm
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
def photos(request):
    """Commencement fotos."""
    user = request.user
    try:
        questionnaire = user.questionnaire
    except Exception:
        questionnaire = None
    if questionnaire:

        instance1 = (questionnaire.photos()[0:1] or (None,))[0]
        instance2 = (questionnaire.photos()[1:2] or (None,))[0]

        if request.method == 'POST':
            form1 = PhotoForm(
                request.POST,
                request.FILES,
                prefix='f1',
                instance=instance1,
                use_required_attribute=REQ_ATTR,
            )
            form2 = PhotoForm(
                request.POST,
                request.FILES,
                prefix='f2',
                instance=instance2,
                use_required_attribute=REQ_ATTR,
            )
            if form1.is_valid() and form2.is_valid():
                doc1 = form1.save(commit=False)
                doc1.questionnaire = user.questionnaire
                doc1.created_by = user
                doc1.updated_by = user
                doc1.save()
                doc1.tags.add('Commencement Photos')
                doc2 = form2.save(commit=False)
                doc2.questionnaire = user.questionnaire
                doc2.created_by = user
                doc2.updated_by = user
                doc2.save()
                doc2.tags.add('Commencement Photos')
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    "Photos saved",
                    extra_tags='alert-success',
                )
                return HttpResponseRedirect(reverse_lazy('home'))
        else:
            form1 = PhotoForm(
                prefix='f1',
                instance=instance1,
                use_required_attribute=REQ_ATTR,
            )
            form2 = PhotoForm(
                prefix='f2',
                instance=instance2,
                use_required_attribute=REQ_ATTR,
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
        request, 'gearup/photos.html', {'form1': form1, 'form2': form2},
    )


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
        finaid = user.questionnaire.finaid
        if request.method == 'POST':
            finaid = request.POST.get('finaid')
            if finaid == 'Yes':
                form = CounselingForm(
                    request.POST, request.FILES, use_required_attribute=REQ_ATTR,
                )
                if form.is_valid():
                    user.questionnaire.finaid = 'Yes'
                    user.questionnaire.save()
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
                    finaid = 'Yes'
            elif finaid == 'No':
                user.questionnaire.finaid = 'No'
                return HttpResponseRedirect(reverse_lazy('home'))
            else:
                form = CounselingForm(use_required_attribute=REQ_ATTR)
                messages.add_message(
                    request,
                    messages.WARNING,
                    "You must choose 'Yes' or 'No'",
                    extra_tags='alert-warning',
                )
        else:
            form = CounselingForm(use_required_attribute=REQ_ATTR)
    else:
        messages.add_message(
            request,
            messages.WARNING,
            "Please submit the Gear Up questionnaire",
            extra_tags='alert-warning',
        )
        return HttpResponseRedirect(reverse_lazy('home'))
    return render(
        request, 'gearup/counseling.html', {'form': form, 'finaid': finaid},
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
                username = form_data['recipients']
                try:
                    recipient = User.objects.get(username=username)
                except Exception:
                    eldap = LDAPManager()
                    result_data = eldap.search(username, field='cn')
                    groups = eldap.get_groups(result_data)
                    recipient = eldap.dj_create(result_data, groups=groups)
                if recipient:
                    note.recipients.add(recipient)
                    messages.add_message(
                        request,
                        messages.SUCCESS,
                        "Note saved. Submit another?",
                        extra_tags='alert-success',
                    )
                else:
                    messages.add_message(
                        request,
                        messages.ERROR,
                        "Note failed. Invalid recipient.",
                        extra_tags='alert-error',
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
        quest = user.questionnaire
    except Exception:
        quest = None
    # fetch student data
    student = get_student(user.id)
    if request.method == 'POST':
        form = QuestionnaireForm(
            request.POST, use_required_attribute=REQ_ATTR, instance=quest,
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
        form = QuestionnaireForm(use_required_attribute=REQ_ATTR, instance=quest)
        pho_form = PhoneticForm(use_required_attribute=REQ_ATTR)
    return render(
        request,
        'gearup/questionnaire.html',
        {
            'form': form,
            'pho_form': pho_form,
            'student': student,
        },
    )
