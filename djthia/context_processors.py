# -*- coding: utf-8 -*-

"""Views for all requests."""

from django.conf import settings
from djthia.core.utils import get_finaid


def finaid(request):
    """Check status and set the template context."""
    context = {}
    if request.user.id:
        status = get_finaid(request.user.id)
        if settings.DEBUG:
            status = True
        context['finaid'] = status

    return context


def sitevars(request):
    """Expose some settings to the template level."""
    context = {}
    context['cia_group'] = settings.CIA_GROUP

    return context
