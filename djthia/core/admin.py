# -*- coding: utf-8 -*-

"""Admin classes for data models."""

from django.contrib import admin
from django.db import models
from django.forms import CheckboxSelectMultiple
from django.utils.safestring import mark_safe

from djthia.core.models import GenericChoice


class GenericChoiceAdmin(admin.ModelAdmin):
    """GenericChoice admin class."""

    list_display = ('name', 'value', 'rank', 'tag_list', 'admin', 'active')
    list_editable = ('active', 'admin')
    list_per_page = 500


admin.site.register(GenericChoice, GenericChoiceAdmin)
