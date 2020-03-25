# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models


class Checklist(models.Model):
    """Graduate gearup check list for graduation."""

    created_by = models.ForeignKey(
        User,
        verbose_name="Created by",
        related_name='checklist_created_by',
        editable=False,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    updated_by = models.ForeignKey(
        User,
        verbose_name="Updated by",
        related_name='checklist_updated_by',
        editable=False,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField("Date Created", auto_now_add=True)
    updated_at = models.DateTimeField("Date Updated", auto_now=True)

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
