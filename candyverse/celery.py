import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'candyverse.settings')

app = Celery('candyverse')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Default broker (can be overridden with REDIS_URL env var)
app.conf.broker_url = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')

# Example: run periodic tasks every 5 minutes if using celery beat (configure separately)
# app.conf.beat_schedule = {
#     'recalculate-leaderboard-every-5-minutes': {
#         'task': 'leaderboard.tasks.recalculate_ranks',
#         'schedule': 300.0,
#     },
# }
