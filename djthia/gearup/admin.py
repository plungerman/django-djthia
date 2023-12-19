# -*- coding: utf-8 -*-

from django.contrib import admin
from djthia.gearup.models import Annotation
from djthia.gearup.models import Document
from djthia.gearup.models import Questionnaire


class QuestionnaireAdmin(admin.ModelAdmin):
    """Django admin class for Questionnaire model."""

    model = Questionnaire
    raw_id_fields = ('created_by', 'updated_by')
    list_max_show_all = 500
    list_per_page = 500
    list_display = (
        'last_name',
        'first_name',
        'email',
        'username',
        'created_at',
    )
    ordering = (
        '-created_at',
        'created_by__last_name',
        'created_by__first_name',
    )
    search_fields = (
        'created_by__last_name',
        'created_by__username',
    )


class AnnotationAdmin(admin.ModelAdmin):
    """Django admin class for Annotation model."""

    model = Annotation
    raw_id_fields = ('created_by', 'updated_by')
    list_max_show_all = 500
    list_per_page = 500
    list_display = (
        'last_name',
        'first_name',
        'username',
        'to_list',
        'created_at',
    )
    ordering = (
        '-created_at',
        'created_by__last_name',
        'created_by__first_name',
    )
    search_fields = (
        'created_by__last_name',
        'created_by__username',
    )


class DocumentAdmin(admin.ModelAdmin):
    """Django admin class for Document model."""

    model = Document
    raw_id_fields = ('created_by', 'updated_by')
    list_max_show_all = 500
    list_per_page = 500
    list_display = (
        'created_by',
        'name',
        'phile',
        'questionnaire',
        'tags',
        'created_at',
    )
    ordering = (
        '-created_at',
        'created_by__last_name',
        'created_by__first_name',
    )
    search_fields = (
        'created_by__last_name',
        'created_by__username',
    )


admin.site.register(Annotation, AnnotationAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Questionnaire, QuestionnaireAdmin)
