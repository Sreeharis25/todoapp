"""Tests for task manager app."""
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User

import pytest

from .models import Task, SubTask


pytestmark = pytest.mark.django_db


def get_user_by_id(id):
    return User.objects.get(id=id)


def create_user(username, password):
    return User.objects.create(
        username=username, password=password)


def create_task(title, description, due_date):
    try:
        user = get_user_by_id(1)
    except:
        user = create_user('testuser', 'password123')
    return Task.objects.create(
        title=title, description=description,
        due_date=due_date, user=user)


def get_task_by_id(id):
    return Task.objects.get(id=id)


def test_task_save():
    task = create_task('Task1', 'Description 1', '2018-08-01')
    assert task.title == 'Task1'
    assert task.description == 'Description 1'
    assert task.due_date == '2018-08-01'


def create_sub_task(description):
    try:
        task = get_task_by_id(1)
    except:
        task = create_task('Task1', 'Description 1', '2018-08-01')
    return SubTask.objects.create(
        description=description, task=task)


def test_sub_task_save():
    sub_task = create_sub_task('description')
    assert sub_task.description == 'description'


@pytest.mark.django_db
def test_task_count():
    """
    Test task count.
    """
    assert Task.objects.count() == 0
