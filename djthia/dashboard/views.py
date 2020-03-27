# -*- coding: utf-8 -*-

"""URLs for all views."""

from django.conf import settings
from django.shortcuts import render
from django.urls import reverse_lazy
from djimix.decorators.auth import portal_auth_required


@portal_auth_required(
    session_var='DJTHIA_AUTH',
    redirect_url=reverse_lazy('access_denied')
)
def detail(request, oid):
    """Gear up detailed view."""
    return render(request, 'dashboard/detail.html', {})


@portal_auth_required(
    session_var='DJTHIA_AUTH',
    redirect_url=reverse_lazy('access_denied')
)
def home(request):
    """Dashboard home."""
    return render(request, 'dashboard/home.html', {})


@portal_auth_required(
    session_var='DJTHIA_AUTH',
    redirect_url=reverse_lazy('access_denied')
)
def search(request):
    """Generic search."""
    return render(request, 'gearup/search.html', {})
