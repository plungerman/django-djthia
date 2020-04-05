# -*- coding: utf-8 -*-

from django.shortcuts import render
from djthia.core.utils import get_status


def eligibility(view_func):
    """Check the user for eligibility to access the forms."""
    def wrap(request, *args, **kwargs):
        """Wrapper for the decorator."""
        if request.user.id and get_status(request.user.id):
            return view_func(request, *args, **kwargs)
        elif request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            return render(request, 'denied.html')
    return wrap
