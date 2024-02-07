# -*- coding: utf-8 -*-


from datetime import date
from django.conf import settings
from django.shortcuts import render
from django.urls import reverse_lazy
from djthia.gearup.models import Questionnaire
from djtools.decorators.auth import group_required


@group_required(settings.CIA_GROUP)
def detail(request, oid):
    """Gear up detailed view."""
    return render(request, 'dashboard/detail.html', {})


@group_required(settings.CIA_GROUP)
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


@group_required(settings.CIA_GROUP)
def search(request):
    """Generic search."""
    return render(request, 'gearup/search.html', {})
