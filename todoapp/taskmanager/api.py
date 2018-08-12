"""Apis using tastypie for task manager app.."""
from django.contrib.auth.models import User
from django.conf.urls import url

from json import loads

from tastypie.resources import ModelResource
from tastypie.authentication import BasicAuthentication, Authentication
from tastypie.authorization import Authorization
from tastypie.serializers import Serializer
from tastypie import fields
from tastypie.utils import trailing_slash

import utilities
from .utilities import success_response
from .utilities import error_response

import bll as task_bll

from .exceptions import InvalidUserParameters
from .exceptions import UsernameExists
from .exceptions import UnauthorizedUsername
from .exceptions import UnauthorizedPassword
from .exceptions import UserNotActive
from .exceptions import InvalidTaskParameters
from .exceptions import InvalidSubTaskParameters
from .exceptions import InvalidDueDate


from .models import Task, SubTask


class UserResource(ModelResource):
    """User resource class."""

    class Meta:
        """Meta class."""

        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['is_staff', 'is_active', 'is_superuser']
        authentication = BasicAuthentication()
        authorization = Authorization()
        serializer = Serializer(formats=['json', ])

    def prepend_urls(self):
        """Override urls for user login, signup and logout."""
        return [
            url(r"^(?P<resource_name>%s)/signup%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('signup'), name="api_signup"),
            url(r"^(?P<resource_name>%s)/login%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('login'), name="api_login"),
            url(r'^(?P<resource_name>%s)/logout%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('logout'), name='api_logout'),
        ]

    def signup(self, request, **kwargs):
        """For user signup.

        Input params:
            username(str): Username of the user.
            password(password): password for the user.
            first_name(str): First for the user.
            email(email): Email id of the user
        Response:
            data(json): dictionary with,
                success: bool value showing success msg.
                user: User resource uri.
        """
        self.method_check(request, allowed=['post'])

        request_dict = {}
        try:
            request_dict['received_data'] = loads(request.body)
            request_dict['mandatory_params'] = [
                ('username', 'str'), ('password', 'password'),
                ('first_name', 'str'), ('email', 'email')]
            user_dict = utilities.fetch_request_params(request_dict)

            user_data = task_bll.signup_user(user_dict)
            data = success_response(user_data)
        except(
            KeyError, ValueError, InvalidUserParameters,
                UsernameExists) as e:
            data = error_response(e)

        return data

    def login(self, request, **kwargs):
        """For user login.

        Input params:
            username(str): Username of the user.
            password(password): password of the user.
        Response:
            data(json): dictionary with,
                success: bool value showing success msg.
                user: User resource uri.
        """
        self.method_check(request, allowed=['post'])

        request_dict = {}
        try:
            request_dict['received_data'] = loads(request.body)
            request_dict['mandatory_params'] = [
                ('username', 'str'), ('password', 'password')]
            user_dict = utilities.fetch_request_params(request_dict)
            user_dict['request'] = request

            user_data = task_bll.login_user(user_dict)
            data = success_response(user_data)
        except(
            KeyError, ValueError, UnauthorizedUsername,
                UnauthorizedPassword, UserNotActive) as e:
            data = error_response(e)

        return data

    def logout(self, request, **kwargs):
        """For logout.

        Input:
            request
        Response:
            success
        """
        self.method_check(request, allowed=['get'])

        user_dict = {}
        try:
            user_dict['request'] = request

            user_data = task_bll.logout_user(user_dict)
            data = success_response(user_data)
        except(KeyError, ValueError) as e:
            data = error_response(e)

        return data


class TaskResource(ModelResource):
    """Task resource class."""
    user = fields.ForeignKey(UserResource, 'user')

    class Meta:
        """Meta class."""

        queryset = Task.objects.all()
        resource_name = 'task'
        list_allowed_methods = ['get', 'post', 'put']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        authentication = Authentication()
        authorization = Authorization()
        filtering = {
            "title": ('exact', 'icontains',),
        }
        ordering = ['due_date']
        serializer = Serializer(formats=['json', ])

    def prepend_urls(self):
        """Override urls for geting tasks and task alerts."""
        print self._meta.resource_name
        return [
            url(r"^(?P<resource_name>%s)/get%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_task'), name="api_get_task"),
            url(r"^(?P<resource_name>%s)/alert/get%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_task_alert'), name="api_get_task_alert"),
        ]

    def get_task(self, request, **kwargs):
        """For getting tasks.

        Input params:
            (optional)
            title(str): Title for searching tasks.
            due_date(str): for filter tasks using due date.
            offset(int): offset for the task list.
            limit(int): limit for the task limit.
        Response:
            data(json): dictionary with,
                objects: task details list.
                meta: pagination details.
        """
        self.method_check(request, allowed=['get'])

        request_dict = {}
        try:
            request_dict['received_data'] = request.GET
            request_dict['optional_params'] = [
                ('title', 'str'), ('due_date', 'str'),
                ('offset', 'int'), ('limit', 'int')]
            task_dict = utilities.fetch_request_params(request_dict)

            task_data = task_bll.get_tasks(task_dict)
            data = success_response(task_data)
        except(
            KeyError, ValueError, InvalidTaskParameters,
                InvalidSubTaskParameters, InvalidDueDate) as e:
            data = error_response(e)

        return data

    def get_task_alert(self, request, **kwargs):
        """For task alerts.

        Response:
            data(json): dictionary with,
                objects: task details list.
                meta: pagination details.
        """
        self.method_check(request, allowed=['get'])

        request_dict = {}
        try:
            request_dict['received_data'] = request.GET
            task_dict = utilities.fetch_request_params(request_dict)

            task_data = task_bll.get_alert_needed_tasks(task_dict)
            data = success_response(task_data)
        except(
            KeyError, ValueError, InvalidTaskParameters,
                InvalidSubTaskParameters) as e:
            data = error_response(e)

        return data


class SubTaskResource(ModelResource):
    """Sub Task resource class."""

    task = fields.ForeignKey(TaskResource, 'task')

    class Meta:
        """Meta class."""

        queryset = SubTask.objects.all()
        resource_name = 'subtask'
        authentication = Authentication()
        authorization = Authorization()
        serializer = Serializer(formats=['json', ])
