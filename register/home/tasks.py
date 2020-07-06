from __future__ import absolute_import, unicode_literals
from register.celery import app
from django.core import serializers
import celery
from celery import shared_task
from home.models import Post, Buzz
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings
from django.core.cache import cache


@shared_task(bind=True)
def get_hot_posts(self):
    hot_posts = Post.objects.get_hot()
    cache.set("hot_posts", hot_posts, timeout=None)

@shared_task(bind=True)
def get_top_posts(self):
    pass




