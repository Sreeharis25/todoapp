"""Bll for task manager app."""
from django.db.models import Q
from django.contrib.auth import login, logout

import datetime
from datetime import timedelta

import dal as task_dal

import utilities

from .exceptions import UsernameExists
from .exceptions import UnauthorizedPassword
from .exceptions import UnauthorizedUser
from .exceptions import UserNotActive
from .exceptions import InvalidTaskParameters
from .exceptions import InvalidSubTaskParameters
from .exceptions import InvalidDueDate

from .constants import DUE_DATE_TODAY
from .constants import DUE_DATE_OVERDUE
from .constants import DUE_DATE_THIS_WEEK
from .constants import DUE_DATE_NEXT_WEEK
from .constants import DUE_DATE_THIS_MONTH


def signup_user(user_dict):
    """For signinup user.

    Input Params:
        user_dict (dict): Dictionary with.
            username (str): username for the user
            password(password): password for the user.
            first_name(str): First for the user.
            email(email): Email id of the user
    Returns:
        user_data (dict): Dictionary with.
            success: bool value showing success msg.
            user: User resource uri.
    """
    if task_dal.filter_user_by_username(user_dict['username']).exists():
        raise UsernameExists

    user = task_dal.create_user(user_dict)
    user_data = {
        'success': True,
        'user': '/api/v1/user/' + str(user.id) + '/'
    }

    return user_data


def login_user(user_dict):
    """For user login.

    Input Params:
        user_dict (dict): Dictionary with.
            username (str): username of the user
            password(password): password of the user.
    Returns:
        user_data (dict): Dictionary with.
            success: bool value showing success msg.
            user: User resource uri.
    """
    user = task_dal.get_user_by_username(user_dict['username'])

    if user.check_password(user_dict['password']) is False:
        raise UnauthorizedPassword

    if user.is_active:
        login(user_dict['request'], user)
        user_data = {
            'success': True,
            'user': '/api/v1/user/' + str(user.id) + '/'
        }
    else:
        raise UserNotActive

    return user_data


def logout_user(user_dict):
    """For user logout.

    Input Params:
        user_dict (dict): Dictionary with.
            request
    Returns:
        user_data (dict): Dictionary with.
            success: bool value showing success msg.
    """
    request = user_dict['request']
    if request.user and request.user.is_authenticated():
        logout(request)
        user_data = {'success': True}
    else:
        raise UnauthorizedUser

    return user_data


def get_tasks(task_dict):
    """For getting tasks.

    Input Params:
        task_dict (dict): Dictionary with.
            title(str): Title for searching tasks.
            due_date(str): for filter tasks using due date.
            offset(int): offset for the task list.
            limit(int): limit for the task limit.
    Returns:
        task_dict (dict): Dictionary with.
            objects: Task details list
            meta: pagination data.
    """
    task_dict = setup_task_query(task_dict)

    task_dict['objects'] = task_dal.filter_task_by_query(task_dict['filter'])
    task_dict['count'] = task_dict['objects'].count()
    task_dict['tasks'] = utilities.setup_query_limit(task_dict)

    task_data = {}
    task_data['objects'] = []
    for task in task_dict['tasks']:
        task_details = get_task_details(task)
        task_data['objects'].append(task_details)

    return task_data


def setup_task_query(task_dict):
    """For setting up task query.

    Input Params:
        task_dict (dict): Dictionary with.
            title(str): Title for searching tasks.
            due_date(str): for filter tasks using due date.
            due_date__gte(str):
                for filter tasks using due date greater than date.
    Returns:
        task_dict (dict): Dictionary with.
            collection objects
    """
    task_dict['filter'] = Q()

    if 'title' in task_dict.keys():
        task_dict['filter'] &= (Q(title__icontains=task_dict['title']))
    if 'due_date' in task_dict.keys():
        current_date = datetime.date.today()
        if task_dict['due_date'] == DUE_DATE_TODAY:
            task_dict['filter'] &= (Q(due_date=current_date))
        elif task_dict['due_date'] == DUE_DATE_THIS_WEEK:
            week_start = current_date - timedelta(current_date.weekday())
            week_end = week_start + timedelta(days=7)
            task_dict['filter'] &= (Q(due_date__range=[week_start, week_end]))
        elif task_dict['due_date'] == DUE_DATE_NEXT_WEEK:
            days_ahead = 7 - current_date.weekday()
            #  difference between week day of monday(0) and
            #  current week day and add 7 to it.
            week_start = current_date + timedelta(days_ahead)
            week_end = week_start + timedelta(7)
            task_dict['filter'] &= (Q(due_date__range=[week_start, week_end]))
        elif task_dict['due_date'] == DUE_DATE_THIS_MONTH:
            current_month = current_date.month
            current_year = current_date.year
            task_dict['filter'] &= (
                Q(due_date__month=current_month) & Q(
                    due_date__year=current_year))
        elif task_dict['due_date'] == DUE_DATE_OVERDUE:
            task_dict['filter'] &= (Q(due_date__lte=current_date))
        else:
            raise InvalidDueDate
    if 'due_date__gte' in task_dict.keys():
        task_dict['filter'] &= (Q(due_date__gte=task_dict['due_date__gte']))
    if 'date' in task_dict.keys():
        task_dict['filter'] &= (Q(due_date=task_dict['date']))

    utilities.setup_default_meta_data(task_dict)

    return task_dict


def get_task_details(task):
    """For getting task details.

    Input Params:
        task (obj): Corresponding task objects
    Returns:
        task_details (dict): Dictionary with.
            task details
    """
    try:
        task_resource_uri = '/api/v1/task/' + str(task.id) + '/'
        task_details = {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'due_date': str(task.due_date),
            'alert_hour': str(task.alert_hour),
            'status': task.status,
            'user': '/api/v1/user/' + str(task.user.id) + '/',
            'resource_uri': task_resource_uri,
            'sub_tasks': []
        }
    except:
        raise InvalidTaskParameters
    sub_tasks = task_dal.filter_sub_task_by_task(task)
    for sub_task in sub_tasks:
        try:
            sub_task_details = {
                'description': sub_task.description,
                'status': sub_task.status,
                'resource_uri': '/api/v1/subtask/' + str(sub_task.id) + '/',
                'id': sub_task.id,
                'task': task_resource_uri
            }
            task_details['sub_tasks'].append(sub_task_details)
        except:
            raise InvalidSubTaskParameters

    return task_details


def get_alert_needed_tasks(task_dict):
    """For getting alert needed tasks.

    Input Params:
        task_dict (dict): Dictionary.
    Returns:
        task_dict (dict): Dictionary with.
            objects: Task details list
            meta: Pagination meta data.
    """
    task_data = {}
    task_data['objects'] = []

    current_time = datetime.datetime.now()
    task_dict['due_date__gte'] = current_time

    task_dict = setup_task_query(task_dict)
    task_dict['objects'] = task_dal.filter_task_by_query(task_dict['filter'])
    task_dict['count'] = task_dict['objects'].count()
    task_dict['tasks'] = utilities.setup_query_limit(task_dict)

    for task in task_dict['tasks']:
        alert_datetime = datetime.datetime.combine(
            task.due_date,
            datetime.datetime.min.time()) - timedelta(task.alert_hour)
        if alert_datetime <= current_time:
            task_details = get_task_details(task)
            task_data['objects'].append(task_details)

    return task_data
