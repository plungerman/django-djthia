#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import django
import os
import sys

# load apps
django.setup()

from django.conf import settings
from djthia.gearup.models import Annotation
from djtools.utils.mail import send_mail

# env
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djthia.settings.shell')

DEBUG = settings.DEBUG


def main():
    """Send emails to recipients of thank you notes."""
    notes = Annotation.objects.all()
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


if __name__ == '__main__':

    sys.exit(main())
