# -*- coding: utf-8 -*-

from django import forms

from djthia.gearup.models import Annotation
from djthia.gearup.models import Document
from djthia.gearup.models import Questionnaire
from djtools.fields import BINARY_CHOICES


class QuestionnaireForm(forms.ModelForm):
    """Graduate gear up questionnaire for graduation."""

    '''
    major_minor = forms.TypedChoiceField(
        label="Are your majors and minors correct?",
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect(),
    )
    cap_gown = forms.TypedChoiceField(
        label="Have you order your cap and gown`?",
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect(),
    )
    '''

    class Meta:
        """Information about the form class."""

        model = Questionnaire
        # either fields or exclude is required
        fields = '__all__'


class AnnotationForm(forms.ModelForm):

    class Meta:
        model = Annotation
        fields = ('body',)


class DocumentForm(forms.ModelForm):

    class Meta:
        model = Document
        fields = ('phile',)
