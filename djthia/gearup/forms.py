# -*- coding: utf-8 -*-

from django import forms

from djthia.gearup.models import Questionnaire


class QuestionnaireForm(forms.ModelForm):
    """Graduate gear up questionnaire for graduation."""

    class Meta:
        """Information about the form class."""

        model = Questionnaire
        # either fields or exclude is required
        fields = '__all__'
