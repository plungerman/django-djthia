# -*- coding: utf-8 -*-

from django import forms
from djthia.gearup.models import Annotation
from djthia.gearup.models import Document
from djthia.gearup.models import Questionnaire


class QuestionnaireForm(forms.ModelForm):
    """Graduate gear up questionnaire for graduation."""

    class Meta:
        """Information about the form class."""

        model = Questionnaire
        # either fields or exclude is required
        fields = '__all__'


class AnnotationForm(forms.ModelForm):
    """Thank you notes form."""

    class Meta:
        """Information about the form class."""

        model = Annotation
        fields = ('body',)


class DocumentForm(forms.ModelForm):
    """Document upload form."""

    class Meta:
        """Information about the form class."""

        model = Document
        fields = ('phile',)
