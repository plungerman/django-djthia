#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import django
import os
import sys

# load apps
django.setup()

from django.conf import settings
from djthia.gearup.models import Annotation

# env
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djthia.settings.shell")

DEBUG = settings.DEBUG


def main():
    """Send emails to recipients of thank you notes."""
    notes = Annotation.objects.all()
    for note in notes:
        print(note.created_by, note.status)
        print(note.recipients.all())


if __name__ == "__main__":

    sys.exit(main())
