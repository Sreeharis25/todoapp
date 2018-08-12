"""Models for taskmanager app for todo."""
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from .constants import STATUS_TYPE_CHOICES


class Task(models.Model):
    """Class representing the task data."""

    user = models.ForeignKey(User)
    title = models.CharField(max_length=100, default='')
    description = models.TextField(default='')
    due_date = models.DateField(default='')
    status = models.CharField(
        max_length=20, default='', choices=STATUS_TYPE_CHOICES)
    alert_hour = models.PositiveIntegerField(default=12, null=True, blank=True)

    def __unicode__(self):
        """For representing the object in unicode."""
        return self.title


class SubTask(models.Model):
    """Class representing sub task data."""

    task = models.ForeignKey(Task)
    title = models.CharField(max_length=100, default='')
    description = models.TextField(default='')
    status = models.CharField(
        max_length=20, default='', choices=STATUS_TYPE_CHOICES)

    def __unicode__(self):
        """For representing the object in unicode."""
        return (self.task.title) + ' - ' + (self.title)
