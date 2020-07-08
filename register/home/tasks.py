from __future__ import absolute_import, unicode_literals
from register.celery import app
from django.core import serializers
import celery
from celery import shared_task
from home.models import Post, Buzz
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings
from django.core.cache import cache

# Celery tasks for Post model 

@shared_task(bind=True)
def get_hot_posts(self):
    
    hot_posts = Post.objects.get_hot()
    cache.set("hot_posts", hot_posts, timeout=None)

@shared_task(bind=True)
def get_top_posts(self):
    
    top_posts = Post.objects.get_top()
    cache.set("top_posts", top_posts, timeout=None)
    
@shared_task(bind=True)
def get_trending_words_posts(self):
    
    trending_words_posts = Post.objects.get_trending_words()
    cache.set("trending_words_posts", trending_words_posts, timeout=None)
    
@shared_task(bind=True)
def trending_tags_post(self):
    
    tt_posts = Post.objects.trending_tags()
    cache.set("tt_post", tt_posts, timeout=None)


#  Celery tasks for Buzz model

@shared_task(bind=True)
def get_hot_buzzes(self):
    
    hot_buzzes = Buzz.objects.get_hot()
    cache.set("hot_buzzes", hot_buzzes, timeout=None)
    
@shared_task(bind=True)
def get_top_buzzes(self):
    
    top_buzzes = Buzz.objects.get_top()
    cache.set("top_buzzes", top_buzzes, timeout=None)
    
@shared_task(bind=True)
def get_trending_words_buzzes(self):
    
    trending_words_buzzes = Buzz.objects.get_trending_words()
    cache.set("trending_words_buzzes", trending_words_buzzes, timeout=None)
    
@shared_task(bind=True)
def trending_tags_buzz(self):
    
    tt_buzzes = Buzz.objects.trending_tags()
    cache.set("tt_buzzes", tt_buzzes, timeout=None)
    



