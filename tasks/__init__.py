from os import environ

from celery import Celery

CELERY_BROKER_URL = environ.get('CELERY_BROKER_URL', 'pyamqp://guest:guest@127.0.0.1:5672')
celery_app = Celery('tasks', broker=CELERY_BROKER_URL)

from tasks.arithmetic import calculate
