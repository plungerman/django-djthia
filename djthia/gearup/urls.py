# -*- coding: utf-8 -*-

"""URLs for all views."""

from django.urls import path
from django.views.generic import TemplateView

from djthia.gearup import views


urlpatterns = [
    path(
        '<str:pid>/display/',
        views.home,
        name='gearup_display',
    ),
    path(
        'success/',
        TemplateView.as_view(template_name='gearup/success.html'),
        name='gearup_success',
    ),
    # default home
    path('', views.home, name='gearup_display_no_pid'),
]
