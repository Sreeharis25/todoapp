"""Constants for task manager app."""

DEFAULT_LIMIT = 10
DEFAULT_OFFSET = 0

STATUS_TYPE_PENDING = 'pending'
STATUS_TYPE_COMPLETED = 'completed'

STATUS_TYPE_CHOICES = (
    (STATUS_TYPE_PENDING, 'Pending'),
    (STATUS_TYPE_COMPLETED, 'Completed'))

DUE_DATE_TODAY = 'today'
DUE_DATE_THIS_WEEK = 'this_week'
DUE_DATE_NEXT_WEEK = 'next_week'
DUE_DATE_OVERDUE = 'overdue'
