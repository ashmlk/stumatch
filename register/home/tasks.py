from __future__ import absolute_import, unicode_literals
from register.celery import app
from django.core import serializers
import celery
from celery import shared_task
from home.models import Post, Buzz, Blog, Course, Professors, Review, CourseObject
from main.models import Profile
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings
from django.core.cache import cache, caches
from django.utils import timezone
import datetime, json
from django.db.models import Q, F, Count, Avg, FloatField
from django.contrib.postgres.search import (
    SearchQuery,
    SearchRank,
    SearchVector,
    TrigramSimilarity,
)
from register.mentions import send_mention_notifications, delete_mention_notifications
from home.algo import get_uni_info
from django.db.models import Q, F, Count, Avg, FloatField
from itertools import chain, groupby
from operator import attrgetter
from home.redis_handlers import adjust_course_avg
from assets.assets import UNI_LIST, UNIVERSITY_SLUGS

redis_cache = caches["default"]
redis_client = redis_cache.client.get_client()

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
    uni_list = Profile.objects.values_list("university", flat=True).distinct()

    posts_list = Post.objects.select_related("author").filter(
        author__public=True, author__rank_objects=True, last_edited__gte=time_threshold
    )

    for u in uni_list:

        np = (
            posts_list.annotate(trigram=TrigramSimilarity("author__university", u))
            .filter(
                Q(author__university=u)
                | Q(author__university__unaccent__icontains=u)
                | Q(trigram__gte=0.1)
            )
            .order_by("trigram", "last_edited")
        )

        t = u.lower().replace(" ", "_") + "_post"

        cache.set(u, np, timeout=None)


@shared_task(bind=True)
def async_send_mention_notifications(self, sender_id, post_id):
    send_mention_notifications(sender_id=sender_id, post_id=post_id)


@shared_task(bind=True)
def async_delete_mention_notifications(self, sender_id, post_id, content):
    delete_mention_notifications(sender_id=sender_id, post_id=post_id, content=content)


@shared_task(bind=True)
def universities_list_page_items(self):
    try:
        uni_list = UNI_LIST
        universities_list = {}
        for uni in uni_list:
            universities_list[uni] = {}
            universities_list[uni]["user_count"] = Profile.objects.filter(
                university__iexact=uni
            ).count()
            universities_list[uni]["course_count"] = (
                Course.objects.filter(course_university__iexact=uni)
                .distinct("course_code", "course_instructor", "course_instructor_fn")
                .count()
            )
            universities_list[uni]["data"] = get_uni_info(uni)
        cache.set("university_list_incoming_student_", universities_list, 14400)
    except Exception as e:
        print(e.__class__)
        print(e)


@shared_task(bind=True)
def update_instructor_courses(self,course):
    try:
        ins = Professors.objects.get(
            first_name=course.course_instructor_fn,
            last_name=course.course_instructor,
            university=course.course_university,
        )
        ins.add_to_courses(course)
    except Exception as e:
        print(e)
        print(e.__class__)


@shared_task(bind=True)
def add_user_to_course(self, user, course):
    try:
        if user not in course.enrolled.all():
            course.enrolled.add(user)
    except Exception as e:
        print(e)
    return True


@shared_task(bind=True)
def add_course_to_prof(self, prof, course_obj):
    try:
        prof.add_to_courses(course_bj)
    except Exception as e:
        print(e)
    return True


@shared_task(bind=True)
def adjust_course_average(self, course):
    try:
        adjust_course_avg(course)
    except Exception as e:
        print(e)
    return True

@shared_task(bind=True)
def user_get_or_set_top_school_courses(self, user):
    try:
        c = Course.objects.get_or_set_top_school_courses(user=user)
    except Exception as e:
        print(e)
        
        
@shared_task(bind=True)
def set_course_objects_top_courses(self, university):
    try:
        courses_id = list (
            CourseObject.objects.filter(
                university_slug__unaccent__iexact=university
            )
            .annotate(enrolled_students=Count("enrolled"))
            .order_by("-enrolled_students")
            .values("id")
        )

        redis_client.hset(
            "cobj-",
            university,
            json.dumps(courses_id)
        )
    except Exception as e:
        print(e)
    
    return True
        