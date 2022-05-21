"""
    Config for celery app. Connecting scheduled tasks
"""


import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exchange_api.settings')

app = Celery('exchange_api')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'get-currency-by-api-every-night': {
        'task': 'currency_exchange.tasks.download_exchange_rates',
        'schedule': crontab(minute='*/60'),
    }
}