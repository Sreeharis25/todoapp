"""Admin for task manager."""
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Task
from .models import SubTask


admin.site.register(Task)
admin.site.register(SubTask)
