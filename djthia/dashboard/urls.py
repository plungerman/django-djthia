# -*- coding: utf-8 -*-

"""URLs for all views."""

from django.conf.urls import path

from djthia.dashboard import views


urlpatterns = [
    path('search/', views.search, name='gearup_search'),
    path('', views.home, name='home'),
]
