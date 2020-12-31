from __future__ import absolute_import, unicode_literals
from register.celery import app
from django.core import serializers
import celery
from celery import shared_task
from home.models import Post, Buzz, Blog, Course, Professors, Review
from main.models import Profile
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings
from django.core.cache import cache
from django.utils import timezone
import datetime
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

UNI_LIST = [
    "Acadia University",
    "Alberta University of the Arts",
    "Algoma University",
    "Athabasca University",
    "Atlantic School of Theology",
    "Bishop's University",
    "Booth University College",
    "Brandon University",
    "Brock University",
    "Canadian Mennonite University",
    "Cape Breton University",
    "Capilano University",
    "Carleton University",
    "Concordia University",
    "Crandall University",
    "Dalhousie University",
    "Emily Carr University of Art and Design",
    "Fairleigh Dickinson University",
    "Institut national de la recherche scientifique",
    "Kingswood University",
    "Kwantlen Polytechnic University",
    "Lakehead University",
    "Laurentian University",
    "MacEwan University",
    "McGill University",
    "McMaster University",
    "Memorial University of Newfoundland",
    "Mount Allison University",
    "Mount Royal University",
    "Mount Saint Vincent University",
    "New York Institute of Technology",
    "Niagara University",
    "Nipissing University",
    "Nova Scotia College of Art and Design University",
    "Ontario College of Art and Design University",
    "Ontario Tech University",
    "Queen's University at Kingston",
    "Quest University",
    "Redeemer University College",
    "Royal Military College of Canada",
    "Royal Roads University",
    "Ryerson University",
    "Saint Francis Xavier University",
    "Saint Mary's University",
    "Simon Fraser University",
    "St. Stephen's University",
    "St. Thomas University",
    "The King's University",
    "Thompson Rivers University",
    "Trent University",
    "Trinity Western University",
    "Tyndale University",
    "University Canada West",
    "University College of the North",
    "University of Alberta",
    "University of British Columbia",
    "University of Calgary",
    "University of Fredericton",
    "University of Guelph",
    "University of King's College",
    "University of Lethbridge",
    "University of Manitoba",
    "University of New Brunswick",
    "University of Northern British Columbia",
    "University of Ottawa",
    "University of Prince Edward Island",
    "University of Regina",
    "University of Saskatchewan",
    "University of Toronto",
    "University of Victoria",
    "University of Waterloo",
    "University of Western Ontario",
    "University of Windsor",
    "University of Winnipeg",
    "University of the Fraser Valley",
    "Université Laval",
    "Université Sainte-Anne",
    "Université de Moncton",
    "Université de Montréal",
    "Université de Sherbrooke",
    "Université de l'Ontario français",
    "Université du Québec en Abitibi-Témiscamingue",
    "Université du Québec en Outaouais",
    "Université du Québec à Chicoutimi",
    "Université du Québec à Montréal",
    "Université du Québec à Rimouski",
    "Université du Québec à Trois-Rivières",
    "Vancouver Island University",
    "Wilfrid Laurier University",
    "York University",
    "Yukon University",
    "École de technologie supérieure",
    "École nationale d'administration publique",
]


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
def update_instructor_courses(course):
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
def add_user_to_course(user, course):
    if not user in course.enrolled.all():
        course.enrolled.add(user)
