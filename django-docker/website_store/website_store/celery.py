import os

from celery import Celery

# from mini_app.tasks import consumer_basket_rabbit


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website_store.settings')

app = Celery('website_store')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Запуск Фоновой задачи для прослушивания сообщений
# consumer_basket_rabbit.delay()