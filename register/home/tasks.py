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
from register.mentions import send_mention_notifications, delete_mention_notifications, update_mention_notifications, delete_mention_notifications_comments, send_mention_notifications_comments
from home.algo import get_uni_info
from django.db.models import Q, F, Count, Avg, FloatField
from itertools import chain, groupby
from operator import attrgetter
from home.redis_handlers import adjust_course_avg_hash, update_course_reviews_cache
from assets.assets import UNI_LIST, UNIVERSITY_SLUGS
from .notifications import send_comment_notification, send_reply_notification

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
def async_update_mention_notifications(self, post_id, old_content):
    update_mention_notifications(post_id=post_id, old_content=old_content)    


@shared_task(bind=True)
def async_send_mention_notifications_comments(self, sender_id, post_id, comment_id):
    send_mention_notifications_comments(sender_id=sender_id, post_id=post_id)


@shared_task(bind=True)
def async_delete_mention_notifications_comments(self, sender_id, post_id, comment_body):
    delete_mention_notifications_comments(sender_id=sender_id, post_id=post_id, content=content)
    
@shared_task(bind=True)
def async_send_notifications_comments(self, sender_id, post_id, comment_id):
    send_comment_notification(sender_id=sender_id, post_id=post_id)
    
@shared_task(bind=True)
def async_send_notifications_comments_reply(self, sender_id, post_id, reply_id, parent_comment_id):
    send_reply_notification(sender_id=sender_id, post_id=post_id, reply_id=reply_id, parent_comment_id=parent_comment_id)
                               
@shared_task(bind=True)
def async_delete_notifications_comments(self, sender_id, post_id, comment_body):
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
        return e
    return True


@shared_task(bind=True)
def add_user_to_course(self, user_id, course_obj_id):
    try:
        user = Profile.objects.get(id=user_id)
        course = CourseObject.objects.get(id=course_obj_id)
        if user not in course.enrolled.all():
            course.enrolled.add(user)
    except Exception as e:
        return e
    return True

@shared_task(bind=True)
def remove_user_from_course(self, user_id, course_init_id, course_new_id=None, course_obj_new_id=None, complete=False):
    try:
        course_init = Course.objects.get(id=course_init_id)
        user = Profile.objects.get(id=user_id)
        if not complete: # if it is not complete removal, remove from old course and add to new
            if course_new_id != None:
                course_new = Course.objects.get(id=course_new_id)
            if course_obj_new_id != None:
                course_obj_new = CourseObject.objects.get(id=course_obj_new_id)
            if (course_init.course_university != course_new.course_university) or (course_init.course_code != course_new.course_code):
                course_obj_old = CourseObject.object.get_or_create(
                            code__iexact=course_init.course_code, university__iexact=course_init.course_university
                        )
                course_obj_old.enrolled.remove(user)
                course_obj_new.enrolled.add(user)
        else: # if it is complete removal, remove form course_object
            course_obj, crc = CourseObject.object.get_or_create(
                    code__iexact=code, university__iexact=course.course_university
                )  
            course_obj.enrolled.remove(user)
    except Exception as e:
        return "Error in removing/adding user to edited course - " + str(e)
    return True

@shared_task(bind=True)
def add_course_to_prof(self, prof_id, course_obj_id):
    try:
        prof = Professors.objects.get(id=prof_id)
        course_obj = CourseObject.objects.get(id=course_obj_id)
        prof.add_to_courses(course_obj)
    except Exception as e:
        return e
    return True


@shared_task(bind=True)
def user_get_or_set_top_school_courses(self, user_id):
    try:
        user = Profile.objects.get(id=user_id)
        top_courses = list( 
            Course.objects
            .prefetch_related('profiles').filter(
                course_university__unaccent__iexact=user.university
            )
            .exclude(course_code__in=[c.course_code for c in user.courses.all()])
            .annotate(enrolled_students=Count("profiles__id"))
            .order_by("-enrolled_students")
            .values("id")
        )

        redis_client.hset(
            "user-",
            "{}-top-school-courses".format(user.get_hashid()),
            json.dumps(top_courses)
            )
        
    except Exception as e:
        return e
    return True
        
        
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
        return e
    return True
        
    