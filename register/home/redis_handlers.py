from __future__ import absolute_import, unicode_literals
from home.models import Post, Buzz, Blog, Course, Professors, Review
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
from home.algo import get_uni_info
from django.db.models import Q, F, Count, Avg, FloatField
from itertools import chain, groupby
from operator import attrgetter

# get the redis client to save data to redis
redis_cache = caches["default"]
redis_client = redis_cache.client.get_client()


def update_course_reviews_cache(course, order=None):

    cache_index = {
        None: "",
        "latest": "",
        "cy": "_yr",
    }

    main_qs = Review.objects.select_related("author").filter(
        course_reviews__course_code=course.course_code,
        course_reviews__course_university__iexact=course.course_university,
    )

    # order_by instructor for all review objects
    main_qs2 = main_qs.order_by(
        "course_reviews__course_instructor", "course_reviews__course_instructor_fn",
    )

    # set hash for objects based on creation date
    result = list(main_qs2.order_by("-created_on",).values("id"))
    
    redis_client.hset(
        "cr_",
        "{}_{}".format(course.course_code, course.course_university_slug),
        json.dumps(result),
    )

    # hash the id of review objects based on course year
    result = list(main_qs2.order_by("-year", "-created_on",).values("id"))

    redis_client.hset(
        "cr_",
        "{}_{}_yr".format(course.course_code, course.course_university_slug),
        json.dumps(result),
    )

    # save data for instructor reviews
    instructor_reviews = list(
        main_qs.filter(
            course_reviews__course_instructor_fn=course.course_instructor_fn,
            course_reviews__course_instructor=course.course_instructor,
        )
        .order_by("-created_on")
        .values("id")
    )

    redis_client.hset(
        "cr_",
        "{}_{}_{}".format(
            course.course_code,
            course.course_university_slug,
            course.course_instructor_slug,
        ),
        json.dumps(instructor_reviews),
    )

    # instructor reviews based on year and date of creation
    instructor_reviews = list(
        main_qs.filter(
            course_reviews__course_instructor_fn=course.course_instructor_fn,
            course_reviews__course_instructor=course.course_instructor,
        )
        .order_by("-year", "-created_on")
        .values("id")
    )

    redis_client.hset(
        "cr_",
        "{}_{}_{}_yr".format(
            course.course_code,
            course.course_university_slug,
            course.course_instructor_slug,
        ),
        json.dumps(instructor_reviews),
    )

    # set the total review count for this specific course and instructor
    count = Course.course_reviews.through.objects.filter(
        course__course_code=course.course_code,
        course__course_university__iexact=course.course_university,
        course__course_instructor_fn__iexact=course.course_instructor_fn,
        course__course_instructor__iexact=course.course_instructor,
    ).count()
    redis_client.hset(
        "cr_",
        "count_{}_{}_{}".format(
            course.course_code,
            course.course_university_slug,
            course.course_instructor_slug,
        ),
        count,
    )

    # set the total reviews count for courses with the same code and university
    count = Course.course_reviews.through.objects.filter(
        course__course_code=course.course_code,
        course__course_university__iexact=course.course_university,
    ).count()
    redis_client.hset(
        "cr_",
        "count_{}_{}_all".format(course.course_code, course.course_university_slug),
        count,
    )

    return True

def adjust_course_avg_hash(course):
    r_dic = {
        4: "Easy",
        3: "Medium",
        2: "Hard",
        1: "Most Failed",
        0: None
    }
    total_users = sum_ratings = 0

    avg = list(
        Course.objects.prefetch_related("profiles")
        .filter(
            course_code=course.course_code,
            course_university__iexact=course.course_university,
        )
        .exclude(course_difficulty=0)
        .values("course_difficulty")
        .annotate(count=Count("profiles__id"))
        .order_by("course_difficulty")
    )

    for el in avg:
        total_users += el["count"]
        sum_ratings += int(el["course_difficulty"]) * el["count"]
    avg_cplx = round(sum_ratings / total_users) if total_users != 0 else 0

    avg_ins = list(
        Course.objects.prefetch_related("profiles")
        .filter(
            course_code=course.course_code,
            course_university__iexact=course.course_university,
            course_instructor__iexact=course.course_instructor,
            course_instructor_fn__iexact=course.course_instructor_fn,
        )
        .exclude(course_difficulty=0)
        .values("course_difficulty")
        .annotate(count=Count("profiles__id"))
        .order_by("course_difficulty")
    )
    
    total_users = sum_ratings = 0
    for el in avg_ins:
        total_users += el["count"]
        sum_ratings += int(el["course_difficulty"]) * el["count"]
    avg_cplx_ins = round(sum_ratings / total_users) if total_users != 0 else 0

    redis_client.hset(
        "cavg_",
        "{}-{}".format(
            course.course_code.replace(" ", ""), course.course_university_slug
        ),
        avg_cplx,
    )
    redis_client.hset(
        "cavg_",
        "{}-{}-{}".format(
            course.course_code.replace(" ", ""),
            course.course_university_slug,
            course.course_instructor_slug,
        ),
        avg_cplx_ins,
    )
    
    return True
