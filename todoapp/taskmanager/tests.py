"""Tests for task manager app."""
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from .models import Task, SubTask


@pytest.mark.django_db
def create_task():
    """
    Create a task with the given `title`, description and due_date.
    """
    Task.objects.create(
    	title='Task1', description='Description 1', due_date='2018-08-01')


def get_task_by_id():
    """
    Get a task by id.
    """
    return Task.objects.get(id=id)



@pytest.mark.django_db
def create_sub_task():
    """
    Create a sub task with the given `title`, description and task.
    """
    task = get_task_by_id(1)
    SubTask.objects.create(
    	title='title', description='description', task=task)


@pytest.mark.django_db
def test_task_count():
    """
    Test task count.
    """
    assert Task.objects.count() == 0