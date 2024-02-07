# -*- coding: utf-8 -*-

"""Views for all requests."""

from django.conf import settings


def sitevars(request):
    """Expose some settings to the template level."""
    context = {}
    context['cia_group'] = settings.CIA_GROUP

    return context
