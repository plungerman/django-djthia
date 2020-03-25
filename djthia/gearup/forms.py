# -*- coding: utf-8 -*-

from django import forms

from djthia.gearup.models import CheckList


class CheckListForm(forms.ModelForm):
    """Graduate Gear up form."""

    class Meta:
        """Information about the form class."""

        model = CheckList
        # either fields or exclude is required
        fields = '__all__'
