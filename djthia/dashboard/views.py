# -*- coding: utf-8 -*-


from datetime import date
from django.conf import settings
from django.shortcuts import render
from django.urls import reverse_lazy
from djthia.gearup.models import Annotation
from djthia.gearup.models import Questionnaire
from djtools.decorators.auth import group_required


@group_required(settings.CIA_GROUP)
def detail(request, oid):
    """Gear up detailed view."""
    return render(request, 'dashboard/detail.html', {})


@group_required(settings.CIA_GROUP)
def home(request):
    """Dashboard home."""
    if settings.DEBUG:
        quests = Questionnaire.objects.all()
    else:
        quests = Questionnaire.objects.filter(created_at__year=date.today().year)
    return render(
        request, 'dashboard/home.html', { 'quests': quests,},
    )


@group_required(settings.CIA_GROUP)
def print_notes(request):
    """Send emails to recipients of thank you notes."""
    notes = Annotation.objects.filter(created_at__year='2024')
    '''
    for note in notes:
        if note.status:
            to = [note.recipients.all()[0].email]
            frum = note.questionnaire.email
            if not frum:
                frum = note.created_by.email
            if DEBUG:
                note.to = to
                note.frum = frum
                to = [settings.MANAGERS[0][1]]
            subject = "A Thank You Note from {0} {1}".format(
                note.created_by.first_name, note.created_by.last_name,
            )
            print(to, frum, subject)
            send_mail(
                None,
                to,
                subject,
                frum,
                'gearup/notes_email.html',
                note,
                reply_to=[frum,],
                bcc=bcc,
            )
            note.status = False
            note.save()
    '''
    return render(request, 'dashboard/print_notes.html', {'notes': notes})


@group_required(settings.CIA_GROUP)
def search(request):
    """Generic search."""
    return render(request, 'gearup/search.html', {})
