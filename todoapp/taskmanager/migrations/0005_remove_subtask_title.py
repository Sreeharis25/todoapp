# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-13 03:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taskmanager', '0004_auto_20180812_1311'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subtask',
            name='title',
        ),
    ]
