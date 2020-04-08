# -*- coding: utf-8 -*-

from django import forms
from django.utils.safestring import mark_safe
from djthia.core.utils import get_facstaff
from djthia.gearup.models import CAP_GOWN_SHIPPING
from djthia.gearup.models import Annotation
from djthia.gearup.models import Document
from djthia.gearup.models import Questionnaire
from djthia.gearup.models import STATUS_CHOICES
from djtools.fields import BINARY_CHOICES


class CapGownForm(forms.ModelForm):
    """Cap and Gown form, a subset of the Questionnaire data model."""

    cap_gown = forms.ChoiceField(
        label="Have you ordered your Cap and Gown?",
        widget=forms.RadioSelect,
        choices=BINARY_CHOICES,
        help_text=mark_safe("""
            If 'No', you can do so
            <a href='http://colleges.herffjones.com/college/carthage/' target='_blank'>here</a>.
            All orders will be shipped beginning May 4.
            Make sure to wear your regalia during the virtual ceremony,
            as graduates will perform the symbolic tradition of moving your
            tassels signaling you've obtained your degree.
        """),
        required=True,
    )
    cap_gown_shipping = forms.ChoiceField(
        label="Where would you like your cap and gown shipped?",
        widget=forms.RadioSelect,
        choices=CAP_GOWN_SHIPPING,
        required=False,
    )

    class Meta:
        """Information about the form class."""

        model = Questionnaire
        fields = ('cap_gown', 'cap_gown_shipping', 'address_cap_gown')

    def clean_cap_gown_shipping(self):
        """Confirm that they have choosen a shipping address if need be."""
        cd = self.cleaned_data
        shipping = cd.get('cap_gown_shipping')
        if cd.get('cap_gown') == 'Yes' and not shipping:
            self.add_error('cap_gown_shipping', "Choose a shipping address")

        return shipping

    def clean_address_cap_gown(self):
        """Confirm that they have provided a shipping address if need be."""
        cd = self.cleaned_data
        address = cd.get('address_cap_gown')
        if cd.get('cap_gown_shipping') == 'address_cap_gown' and not address:
            self.add_error('address_cap_gown', "Provide a shipping address")

        return address


class AnnotationForm(forms.ModelForm):
    """Thank you notes form."""

    recipients = forms.CharField(
        label="Recipient",
        widget=forms.Select(choices=get_facstaff()),
        required=True,
    )

    class Meta:
        """Information about the form class."""

        model = Annotation
        fields = ('recipients', 'body')


class DocumentForm(forms.ModelForm):
    """Document upload form."""

    class Meta:
        """Information about the form class."""

        model = Document
        fields = ('phile',)


class PhoneticForm(DocumentForm):
    """Phonetic pronunciation audio file upload form."""

    phile = forms.FileField(
        label="Upload an mp3 or video with the pronunciation",
    )


class PhotoForm(DocumentForm):
    """Commencement photos upload form."""

    phile = forms.FileField(
        label="Photo file",
        required=False,
        help_text="jpg format",
    )


class QuestionnaireForm(forms.ModelForm):
    """Graduate gear up questionnaire for graduation."""

    status_postgrad = forms.ChoiceField(
        label="""
            Which of the following BEST describes your PRIMARY current status?
        """,
        widget=forms.RadioSelect,
        choices=STATUS_CHOICES,
        required=True,
    )
    major_minor = forms.ChoiceField(
        label="Are your majors and minors correct?",
        widget=forms.RadioSelect,
        choices=BINARY_CHOICES,
        required=True,
        help_text=mark_safe("""
        If your majors and/or minors are incorrect, please contact
        <a href="mailto:registrar@carthage.edu">the registrar</a>.
        """),
    )

    class Meta:
        """Information about the form class."""

        model = Questionnaire
        exclude = (
            ' clubs_orgs', 'cap_gown', 'cap_gown_shipping', 'address_cap_gown',
        )
