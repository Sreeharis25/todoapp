"""Celery for pragati."""
from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'todoapp.settings')

broker_url = 'redis://localhost:6379/0'

app = Celery(
    'todoapp',
    broker=broker_url,
    include=['taskmanager.celery_tasks'])

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
# lambda: settings.base.INSTALLED_APPS


if __name__ == '__main__':
    app.start()


@app.task(bind=True)
def debug_task(self):
    """For debuging task."""
    print('Request: {0!r}'.format(self.request))
