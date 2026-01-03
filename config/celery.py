"""
Celery configuration for Investment Platform project.
"""

import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('investment_platform')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Celery Beat schedule for periodic tasks
app.conf.beat_schedule = {
    'update-prices-hourly': {
        'task': 'apps.users.tasks.update_crypto_and_exchange_rates',
        'schedule': crontab(minute=0),  # Run every hour at :00 minutes
    },
}

app.conf.timezone = 'America/New_York'
