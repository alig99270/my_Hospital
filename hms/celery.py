"""
Celery configuration for Hospital Management System.

This module sets up Celery for asynchronous task processing,
including appointment reminders, notifications, and report generation.
"""
import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hms.settings')

app = Celery('hms')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Debug task to test Celery configuration."""
    print(f'Request: {self.request!r}')


# Example of periodic task schedule (can also be defined in settings.py)
# app.conf.beat_schedule = {
#     'send-appointment-reminders-every-hour': {
#         'task': 'appointments.tasks.send_appointment_reminders',
#         'schedule': crontab(minute=0),
#     },
#     'cleanup-expired-tokens-daily': {
#         'task': 'accounts.tasks.cleanup_expired_tokens',
#         'schedule': crontab(hour=3, minute=0),
#     },
# }
