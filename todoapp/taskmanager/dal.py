"""Dal for task manager app."""
from django.contrib.auth.models import User

from .models import Task
from .models import SubTask

from .exceptions import UnauthorizedUsername
from .exceptions import InvalidUserParameters
from .exceptions import InvalidTaskParameters
from .exceptions import InvalidSubTaskParameters


def create_user(user_dict):
	"""For creating user."""
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
	"""For getting all users."""
	users = User.objects.all()


def get_user_by_username(username):
	"""For getting user by username."""
	try:
		user = User.objects.get(username=username)
	except:
		raise UnauthorizedUsername

	return user


def filter_user_by_username(username):
	"""For filtering users by username."""
	try:
		users = User.objects.filter(username=username)
	except:
		raise InvalidUserParameters

	return users

def filter_task_by_query(queryset):
	"""For filtering task by queryset."""
	try:
		tasks = Task.objects.filter(queryset).order_by('due_date')
	except:
		raise InvalidTaskParameters

	return tasks


def filter_sub_task_by_task(task):
	"""For filtering sub tasks by task."""
	try:
		sub_tasks = SubTask.objects.filter(task=task)
	except:
		raise InvalidSubTaskParameters

	return sub_tasks