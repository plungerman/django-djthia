# -*- coding: utf-8 -*-

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from djthia.core.utils import get_status
from djtools.utils.users import in_group


def eligibility(view_func):
    """Check the user for eligibility to access the forms."""
    def _wrap(request, *args, **kwargs):
        """Wrapper for the decorator."""
        cia = in_group(request.user, settings.CIA_GROUP)
        if request.user.id and get_status(request.user.id):
            return view_func(request, *args, **kwargs)
        elif settings.DEBUG:
            return view_func(request, *args, **kwargs)
        else:
            response = render(request, 'denied.html')
            if cia:
                response = HttpResponseRedirect(reverse_lazy('dashboard_home'))
            return response
    return _wrap
