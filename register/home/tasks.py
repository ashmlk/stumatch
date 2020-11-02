from __future__ import absolute_import, unicode_literals
from register.celery import app
from django.core import serializers
import celery
from celery import shared_task
from home.models import Post, Buzz, Blog
from main.models import Profile
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings
from django.core.cache import cache
from django.utils import timezone
import datetime
from django.db.models import Q, F, Count, Avg, FloatField
from django.contrib.postgres.search import (SearchQuery, SearchRank, SearchVector, TrigramSimilarity,)
from register.mentions import send_mention_notifications, delete_mention_notifications

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
  
@shared_task(bind=True)
def uni_posts(self):
    
    time_threshold = timezone.now() - datetime.timedelta(days=5)
    uni_list = Profile.objects.values_list('university', flat=True).distinct()
    
    posts_list = Post.objects.select_related('author').filter(author__public=True, author__rank_objects=True, last_edited__gte=time_threshold)

    for u in uni_list:
        
        np = posts_list.annotate(trigram = TrigramSimilarity(
            'author__university',u
        ))\
        .filter(Q(author__university=u)|Q(author__university__unaccent__icontains=u)|Q(trigram__gte=0.1))\
        .order_by('trigram','last_edited')
        
        t = u.lower().replace(' ','_') +"_post"
        
        cache.set(u,np, timeout=None)


@shared_task(bind=True)
def async_send_mention_notifications(self, sender_id, post_id):
    send_mention_notifications(sender_id=sender_id, post_id=post_id)
    
@shared_task(bind=True)
def async_delete_mention_notifications(self, sender_id, post_id, content):
    delete_mention_notifications(sender_id=sender_id, post_id=post_id, content=content)