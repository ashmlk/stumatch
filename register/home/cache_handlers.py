from __future__ import absolute_import, unicode_literals
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
from home.algo import get_uni_info
from django.db.models import Q, F, Count, Avg, FloatField
from itertools import chain, groupby
from operator import attrgetter

def update_course_reviews_cache(course):
    
    cache_index = {
            None: "",
            "latest":"",
            "cy": "__yr",
        }
    
    main_qs = Review.objects.select_related('author').filter(
        course_reviews__course_code=course.course_code,
        course_reviews__course_university__iexact=course.course_university,
    )
    
    # set cache for objects based on creation date
    qs = main_qs.order_by(
        "course_reviews__course_instructor","course_reviews__course_instructor_fn", "-created_on",
    ).annotate(
        instructor_first_name=F('course_reviews__course_instructor_fn'),
        instructor_last_name=F('course_reviews__course_instructor'),
    )
    
    result = {
        k: list(vs)
        for k, vs in groupby(qs, attrgetter('instructor_last_name','instructor_first_name'))
    }
    cache.set("courses_reviews__{}__{}__all".format(course.course_code, course.course_university_slug), result)
    
    # set cache for objects based on course date
    qs = main_qs.order_by(
        "course_reviews__course_instructor","course_reviews__course_instructor_fn","-year", "-created_on",
    ).annotate(
        instructor_first_name=F('course_reviews__course_instructor_fn'),
        instructor_last_name=F('course_reviews__course_instructor'),
    )
    result = {
        k: list(vs)
        for k, vs in groupby(qs, attrgetter('instructor_last_name','instructor_first_name'))
    }
    cache.set("courses_reviews__{}__{}__all__year".format(course.course_code, course.course_university_slug), result)
    
    # set the total review count for this specific course and instructor
    count = Course.course_reviews.through.objects.filter(
        course__course_code=course.course_code,
        course__course_university__iexact=course.course_university,
        course__course_instructor_fn__iexact=course.course_instructor_fn,
        course__course_instructor__iexact=course.course_instructor,
    ).count()
    cache.set("courses_review__count__{}_{}_{}".format(course.course_university_slug, course.course_code, course.course_instructor_slug), count)
    
    # set the total reviews count for courses with the same code and university
    count = Course.course_reviews.through.objects.filter(
        course__course_code=course.course_code,
        course__course_university__iexact=course.course_university,
    ).count()
    
    cache.set("courses_review__count__{}_{}__all".format(course.course_university_slug, course.course_code), count)