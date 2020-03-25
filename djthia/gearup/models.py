# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from djtools.fields.helpers import upload_to_path

from taggit.managers import TaggableManager


class Questionnaire(models.Model):
    """Graduate gear up questionnaire for graduation."""

    # meta
    created_by = models.ForeignKey(
        User,
        verbose_name="Created by",
        related_name='created_by',
        editable=False,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    updated_by = models.ForeignKey(
        User,
        verbose_name="Updated by",
        related_name='updated_by',
        editable=False,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField("Date Created", auto_now_add=True)
    updated_at = models.DateTimeField("Date Updated", auto_now=True)
    # core
    name_full
    name_phonetic
    major_minor
    address_mailing
    address_permanent
    email
    phone
    guardian1
    guardian2
    name_spouse
    year_spouse
    marriage_anniversary
    status_postgrad
    graduate_school_name
    graduate_school_program
    graduate_school_address
    graduate_school_city
    graduate_school_state
    graduate_school_country
    graduate_school_email
    employer_name
    employer_address
    employer_city
    employer_state
    employer_country
    employer_email
    employer_job_title
    clubs_orgs
    gift
    color
    speaker
    # notes are FK from Comments data model
    counseling
    cap_gown

    class Meta:
        """Information about the data model class."""

        ordering = ['-created_at']
        get_latest_by = 'created_at'

    def __unicode__(self):
        """Default data for display."""
        return self.created_by.username

    def get_absolute_url(self):
        """Absoluate URL for UI level."""
        return ('gearup_detail', [str(self.id)])


class Annotation(models.Model):

    alert = models.ForeignKey(
        Alert, related_name='notes', on_delete=models.CASCADE
    )
    created_by = models.ForeignKey(
        User, verbose_name="Created by",
        related_name='note_creator',
        on_delete=models.PROTECT
    )
    updated_by = models.ForeignKey(
        User, verbose_name="Updated by", related_name='note_updated',
        on_delete=models.CASCADE, null=True, blank=True
    )
    created_at = models.DateTimeField(
        "Date Created", auto_now_add=True
    )
    updated_at = models.DateTimeField(
        "Date Updated", auto_now=True
    )
    recipients = models.ManyToManyField(
        User, blank=True
    )
    body = models.TextField()
    status = models.BooleanField(default=True, verbose_name="Active?")
    tags = TaggableManager(blank=True)

    class Meta:
        """Information about the data model class."""
        ordering = ('-created_at',)

    def __str__(self):
        """Default data for display."""
        return "{0}, {1}".format(
            self.created_by.last_name, self.created_by.first_name,
        )


class Document(models.Model):
    """Supporting documents."""

    created_by = models.ForeignKey(
        User,
        verbose_name="Created by",
        related_name='doc_creator',
        on_delete=models.CASCADE,
    )
    updated_by = models.ForeignKey(
        User,
        verbose_name="Updated by",
        related_name='doc_updated',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField("Date Created", auto_now_add=True)
    updated_at = models.DateTimeField("Date Updated", auto_now=True)
    questionnaire = models.ForeignKey(
        Questionnaire,
        related_name='files',
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        "Short description of file",
        max_length=128,
        null=True,
        blank=True,
    )
    phile = models.FileField(
        "Supporting files",
        upload_to=upload_to_path,
        validators=FILE_VALIDATORS,
        max_length=767,
        null=True,
        blank=True,
    )
    tags = TaggableManager(blank=True)

    class Meta:
        """Information about the data model class."""

        ordering = ['-created_at']
        get_latest_by = 'created_at'

    def get_slug(self):
        """Slug for file uploads."""
        return 'gearup-document'

    def __str__(self):
        """Default data for display."""
        return str(self.alert)
