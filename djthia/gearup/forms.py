# -*- coding: utf-8 -*-

from django import forms
from djthia.gearup.models import Annotation
from djthia.gearup.models import CAP_GOWN_SHIPPING
from djthia.gearup.models import Document
from djthia.gearup.models import Questionnaire
from djtools.fields import BINARY_CHOICES


class CapGownForm(forms.ModelForm):
    """Cap and Gown form, a subset of the Questionnaire data model."""

    cap_gown = forms.ChoiceField(
        label="Have you ordered your Cap and Gown?",
        widget=forms.RadioSelect,
        choices=BINARY_CHOICES,
        required=True,
    )
    cap_gown_shipping = forms.ChoiceField(
        label="Where would you like your cap and gown shipped?",
        widget=forms.RadioSelect,
        choices=CAP_GOWN_SHIPPING,
        required=True,
    )

    class Meta:
        """Information about the form class."""

        model = Questionnaire
        fields = ('cap_gown', 'cap_gown_shipping', 'address_cap_gown')


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


class QuestionnaireForm(forms.ModelForm):
    """Graduate gear up questionnaire for graduation."""

    major_minor = forms.ChoiceField(
        label="Are your majors and minors correct?",
        widget=forms.RadioSelect,
        choices=BINARY_CHOICES,
        required=True,
    )

    class Meta:
        """Information about the form class."""

        model = Questionnaire
        exclude = (
            ' clubs_orgs', 'cap_gown', 'cap_gown_shipping', 'address_cap_gown',
        )
