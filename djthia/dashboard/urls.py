# -*- coding: utf-8 -*-

"""URLs for all views."""

from django.urls import path
from djthia.dashboard import views


urlpatterns = [
    path('<str:oid>/detail/', views.detail, name='gearup_detail'),
    path('search/', views.search, name='gearup_search'),
    path('notes/', views.print_notes, name='print_notes'),
    path('', views.home, name='dashboard_home'),
]
