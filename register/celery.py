from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
import django

app = Celery('register')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


