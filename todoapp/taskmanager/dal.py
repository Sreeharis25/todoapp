"""Dal for task manager app."""
from django.contrib.auth.models import User

from .models import Task
from .models import SubTask

from .exceptions import UnauthorizedUsername
from .exceptions import InvalidUserParameters
from .exceptions import InvalidTaskParameters
from .exceptions import InvalidSubTaskParameters


def create_user(user_dict):
    """For creating user.

    Input Params:
        user_dict (dict): Dictionary with.
            username (str): username for the user
            password(password): password for the user.
            first_name(str): First for the user.
            email(email): Email id of the user
    Returns:
        (obj): user object.
    """
    try:
        user = User(
            username=user_dict['username'],
            email=user_dict['email'],
            first_name=user_dict['first_name'])
        user.set_password(user_dict['password'])
        user.save()
    except:
        raise InvalidUserParameters

    return user


def get_all_users():
    """For getting all users.

    Returns:
        (obj): user objects.
    """
    users = User.objects.all()

    return users


def get_user_by_username(username):
    """For getting user by username.

    Input Params:
        username (str): username for the user
    Returns:
        (obj): user object.
    """
    try:
        user = User.objects.get(username=username)
    except:
        raise UnauthorizedUsername

    return user


def filter_user_by_username(username):
    """For filtering users by username.

    Input Params:
        username (str): username for the user
    Returns:
        (obj): user objects.
    """
    try:
        users = User.objects.filter(username=username)
    except:
        raise InvalidUserParameters

    return users


def filter_task_by_query(queryset):
    """For filtering task by queryset.

    Input Params:
        queryset (query): fltering query
    Returns:
        (obj): task objects.
    """
    try:
        tasks = Task.objects.filter(queryset).order_by('due_date')
    except:
        raise InvalidTaskParameters

    return tasks


def filter_sub_task_by_task(task):
    """For filtering sub tasks by task.

    Input Params:
        task (obj): task objects
    Returns:
        (obj): sub task objects.
    """
    try:
        sub_tasks = SubTask.objects.filter(task=task)
    except:
        raise InvalidSubTaskParameters

    return sub_tasks
