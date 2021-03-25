# -*- coding: utf-8 -*-


from datetime import date
from django.conf import settings
from django.shortcuts import render
from django.urls import reverse_lazy
from djauth.decorators import portal_auth_required
from djthia.gearup.models import Questionnaire


@portal_auth_required(
    group=settings.CIA_GROUP,
    session_var='DJTHIA_AUTH',
    redirect_url=reverse_lazy('access_denied'),
)
def detail(request, oid):
    """Gear up detailed view."""
    return render(request, 'dashboard/detail.html', {})


@portal_auth_required(
    group=settings.CIA_GROUP,
    session_var='DJTHIA_AUTH',
    redirect_url=reverse_lazy('access_denied'),
)
def home(request):
    """Dashboard home."""
    return render(
        request,
        'dashboard/home.html',
        {
            'quests': Questionnaire.objects.filter(
                created_at__year=date.today().year,
            )

        },
    )


@portal_auth_required(
    group=settings.CIA_GROUP,
    session_var='DJTHIA_AUTH',
    redirect_url=reverse_lazy('access_denied'),
)
def search(request):
    """Generic search."""
    return render(request, 'gearup/search.html', {})
