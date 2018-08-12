"""For managing celery tasks for todoapp."""
from __future__ import absolute_import

from celery.task.schedules import crontab
from celery.decorators import periodic_task

from dateutil import relativedelta
import datetime

from .models import Task

from .constants import STATUS_TYPE_COMPLETED


@periodic_task(
    run_every=(crontab(hour="*", minute="*", day_of_week="*")),
    name="task cleaning", ignore_result=True)
def delete_task():
    """Sample periodic tasks."""
    print 'deleting...'
    previous_month_date = \
        datetime.date.today() - relativedelta.relativedelta(months=1)
    tasks = Task.objects.filter(
        status=STATUS_TYPE_COMPLETED, due_date__lte=previous_month_date)
    tasks.delete()

    print 'Sucess'
