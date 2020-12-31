from django.db import models
from django.utils import timezone
from main.models import Profile, BookmarkPost, BookmarkBlog, BookmarkBuzz
from django.urls import reverse
from django.core.cache import cache
from django.core.validators import (
    MaxLengthValidator,
    MinValueValidator,
    MaxValueValidator,
)
from django.db.models import Q, F, Count, Avg, FloatField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.functions import Cast
from django.template.defaultfilters import slugify
import uuid
import math
import secrets
from django_uuid_upload import upload_to_uuid
import uuid
import datetime
from math import log
import pytz
from dateutil import tz
import PIL
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
import io
from hashids import Hashids
from ckeditor_uploader.fields import RichTextUploadingField
import readtime
from taggit_selectize.managers import TaggableManager
from django.contrib.postgres.search import (
    SearchQuery,
    SearchRank,
    SearchVector,
    TrigramSimilarity,
)
from django.contrib.postgres.aggregates import StringAgg
from django.contrib.postgres.indexes import GinIndex
import django.contrib.postgres.search as pg_search
from django.db.models.functions import Greatest
from collections import Counter
from itertools import chain, groupby
from operator import attrgetter
import nltk
from nltk.collocations import *
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import string
from math import log
from home.algo import (
    score,
    _commonwords,
    common_words,
    epoch_seconds,
    top_score_posts,
    hot_buzz,
    top_buzz,
)
from friendship.models import Friend, Follow, Block, FriendshipRequest

hashids = Hashids(salt="v2ga hoei232q3r prb23lqep weprhza9", min_length=8)

hashid_list = Hashids(salt="e5896e mqwefv0t mvSOUH b90 NS0ds90", min_length=16)


def max_value_current_year():
    return datetime.date.today().year + 1


# CUSTOM MODEL MANAGERS
class PostManager(models.Manager):
    def search_topresult(self, search_text):

        search_vectors = SearchVector(
            "title", weight="A", config="english"
        ) + SearchVector(
            StringAgg("content", delimiter=" "), weight="B", config="english"
        )
        search_query = SearchQuery(search_text, config="english")
        search_rank = SearchRank(search_vectors, search_query)
        trigram = TrigramSimilarity("title", search_text) + (
            TrigramSimilarity("content", search_text)
        )
        qs = (
            self.get_queryset()
            .filter(sv=search_query, author__public=True)
            .annotate(rank=search_rank, trigram=trigram, bs=Greatest("rank", "trigram"))
            .filter(Q(bs__gte=0.2))
            .order_by("-bs")[:5]
        )
        if qs.count() < 1:
            return self.search(search_text)[:5]
        else:
            return qs

    def search(self, search_text):
        search_vectors = SearchVector(
            "title", weight="A", config="english"
        ) + SearchVector(
            StringAgg("content", delimiter=" "), weight="B", config="english"
        )
        search_query = SearchQuery(search_text, config="english")
        search_rank = SearchRank(search_vectors, search_query)
        trigram = TrigramSimilarity("title", search_text) + (
            TrigramSimilarity("content", search_text)
        )
        qs = (
            self.get_queryset()
            .filter(sv=search_query, author__public=True)
            .annotate(rank=search_rank, trigram=trigram, bs=Greatest("rank", "trigram"))
            .filter(Q(bs__gte=0.1))
            .order_by("-bs")
        )

        return qs

    def get_hot(self):

        qs = (
            self.get_queryset()
            .select_related("author")
            .filter(author__rank_objects=True, author__public=True)
        )

        qs_list = list(qs)
        sorted_post = sorted(qs_list, key=lambda p: p.hot(), reverse=True)

        sorted_post_ids = [p.id for p in sorted_post]

        return sorted_post_ids

    def get_top(self):

        time_threshold = timezone.now() - datetime.timedelta(days=6)

        qs = (
            self.get_queryset()
            .select_related("author")
            .filter(
                author__public=True,
                author__rank_objects=True,
                last_edited__gte=time_threshold,
            )
        )

        qs_list = list(qs)
        sorted_post = sorted(qs_list, key=lambda p: p.top(), reverse=True)

        sorted_post_ids = [p.id for p in sorted_post]

        return sorted_post_ids

    def get_top_for_user(self, user):

        qs = user.post_set.all()

        qs_list = list(qs)
        sorted_post = sorted(qs_list, key=lambda p: p.top(), reverse=True)

        sorted_post_ids = [p.id for p in sorted_post]

        return sorted_post_ids

    def get_trending_words(self):

        time_threshold = timezone.now() - datetime.timedelta(days=3)

        qs = self.get_queryset().filter(
            author__public=True, last_edited__gte=time_threshold
        )

        words = list()

        for p in qs:
            words.append((p.content).split())
        words = chain.from_iterable(words)
        result = _commonwords(" ".join(words))
        return result

    def trending_tags(self):

        time_threshold = timezone.now() - datetime.timedelta(days=3)
        qs = self.get_queryset().filter(
            author__public=True, last_edited__gte=time_threshold
        )
        tags = Post.tags.most_common(extra_filters={"post__in": qs})[:5]

        return tags


class CommentManager(models.Manager):
    def most_recent_comments_by_friends(post_ids, friends_ids):

        qs = self.get_queryset().raw(
            "SELECT post_id, id, text FROM joincampus_comment\
                (SELECT post_id, id, text, rank() OVER (PARTITION BY post_id ORDER BY id DESC)\
                FROM joincampus_comment WHERE post_id in %s AND name_id in %s) sub\
                WHERE rank <= 2\
                ORDER BY post_id, id",
            params=[post_ids, friends_ids],
        )

        return qs


class BlogManager(models.Manager):
    def search_topresult(self, search_text):

        search_vectors = SearchVector(
            "title", weight="A", config="english"
        ) + SearchVector(
            StringAgg("content", delimiter=" "), weight="B", config="english"
        )
        search_query = SearchQuery(search_text, config="english")
        search_rank = SearchRank(search_vectors, search_query)
        trigram = TrigramSimilarity("title", search_text)

        qs = (
            self.get_queryset()
            .filter(sv=search_query)
            .annotate(rank=search_rank, trigram=trigram, bs=Greatest("rank", "trigram"))
            .filter(Q(bs__gte=0.2))
            .order_by("-bs")[:5]
        )
        if qs.count() < 1:
            return self.search(search_text)[:5]
        else:
            return qs

    def search(self, search_text):
        search_vectors = SearchVector(
            "title", weight="A", config="english"
        ) + SearchVector(
            StringAgg("content", delimiter=" "), weight="B", config="english"
        )
        search_query = SearchQuery(search_text, config="english")
        search_rank = SearchRank(search_vectors, search_query)
        trigram = TrigramSimilarity("title", search_text)

        qs = (
            self.get_queryset()
            .filter(sv=search_query)
            .annotate(rank=search_rank, trigram=trigram, bs=Greatest("rank", "trigram"))
            .filter(Q(bs__gte=0.05))
            .order_by("-bs")
        )

        return qs

    def get_blogs(self, user):

        fl = bl = []
        friends = Friend.objects.friends(user)
        blocked = Block.objects.blocking(user)

        if friends:
            for f in friends:
                fl.append(str(f))
        if blocked:
            for b in blocked:
                bl.append(str(b))

        time_threshold = timezone.now() - datetime.timedelta(days=7)

        qs = (
            self.get_queryset()
            .annotate(like_count=Count("likes"))
            .filter(
                (~Q(author__username__in=bl))
                & (
                    (
                        Q(author__username__in=friends)
                        | Q(author__university__iexact=user.university)
                    )
                    & (Q(last_edited__gte=time_threshold))
                )
            )
            .order_by("-last_edited", "like_count")
        )

        return qs


class BuzzManager(models.Manager):
    def search_topresult(self, search_text):

        search_vectors = SearchVector(
            "title", weight="A", config="english"
        ) + SearchVector(
            StringAgg("content", delimiter=" "), weight="B", config="english"
        )
        search_query = SearchQuery(search_text, config="english")
        search_rank = SearchRank(search_vectors, search_query)
        trigram = TrigramSimilarity("title", search_text) + (
            TrigramSimilarity("content", search_text)
        )
        qs = (
            self.get_queryset()
            .filter(sv=search_query, author__public=True)
            .annotate(rank=search_rank, trigram=trigram, bs=Greatest("rank", "trigram"))
            .filter(Q(bs__gte=0.2))
            .order_by("-bs")[:5]
        )
        if qs.count() < 1:
            return self.search(search_text)[:5]
        else:
            return qs

    def search(self, search_text):
        search_vectors = (
            SearchVector("title", weight="A", config="english")
            + SearchVector(
                StringAgg("content", delimiter=" "), weight="B", config="english"
            )
            + SearchVector("nickname", weight="C", config="english")
        )
        search_query = SearchQuery(search_text, config="english")
        search_rank = SearchRank(search_vectors, search_query)
        trigram = TrigramSimilarity("title", search_text) + TrigramSimilarity(
            "nickname", search_text
        )

        qs = (
            self.get_queryset()
            .filter(sv=search_query, author__public=True)
            .annotate(rank=search_rank, trigram=trigram, bs=Greatest("rank", "trigram"))
            .filter(Q(bs__gte=0.05))
            .order_by("-bs")
        )

        return qs

    def get_hot(self):

        qs = (
            self.get_queryset()
            .select_related("author")
            .filter(author__rank_objects=True, author__public=True)
        )

        qs_list = list(qs)
        sorted_buzz = sorted(qs_list, key=lambda p: p.hot(), reverse=True)

        sorted_buzz_ids = [b.id for b in sorted_buzz]

        return sorted_buzz_ids

    def get_top(self):

        time_threshold = timezone.now() - datetime.timedelta(days=3)

        qs = (
            self.get_queryset()
            .select_related("author")
            .filter(
                author__public=True,
                author__rank_objects=True,
                last_edited__gte=time_threshold,
            )
        )

        qs_list = list(qs)
        sorted_buzz = sorted(qs_list, key=lambda p: p.top(), reverse=True)

        sorted_buzz_ids = [b.id for b in sorted_buzz]

        return sorted_buzz_ids

    def get_trending_words(self):

        time_threshold = timezone.now() - datetime.timedelta(days=3)

        qs = self.get_queryset().filter(
            author__public=True, last_edited__gte=time_threshold
        )

        words = list()
        """ 
        for p in qs:
            words.append(common_words(p.content))
        counter = Counter(chain.from_iterable(words))
        result = [word for word, word_count in counter.most_common(11)]
        return result
        """
        for p in qs:
            words.append((p.content).split())
        words = chain.from_iterable(words)
        result = _commonwords(" ".join(words))
        return result

    def trending_tags(self):

        time_threshold = timezone.now() - datetime.timedelta(days=3)
        qs = self.get_queryset().filter(
            author__public=True, last_edited__gte=time_threshold
        )
        tags = Buzz.tags.most_common(extra_filters={"buzz__in": qs})[:5]

        return tags


class CourseManager(models.Manager):
    def search(self, search_text):

        search_vectors = (
            SearchVector("course_code", weight="A", config="english")
            + SearchVector("course_instructor", deweight="C", config="english")
            + SearchVector(
                StringAgg("course_university", delimiter=" "),
                weight="C",
                config="english",
            )
            + SearchVector(
                "course_code", "course_instructor", weight="B", config="english"
            )
            + SearchVector(
                "course_university", "course_instructor", weight="B", config="english"
            )
            + SearchVector(
                "course_code",
                "course_instructor",
                "course_instructor_fn",
                weight="B",
                config="english",
            )
        )

        search_query = SearchQuery(search_text, config="english")
        search_rank = SearchRank(search_vectors, search_query)

        trigram = (
            TrigramSimilarity("course_code", search_text)
            + TrigramSimilarity("course_instructor", search_text)
            + TrigramSimilarity("course_university", search_text)
        )

        ds = self.get_queryset().distinct(
            "course_code", "course_instructor", "course_university"
        )

        qs = (
            self.get_queryset()
            .annotate(rank=search_rank, trigram=trigram, bs=Greatest("trigram", "rank"))
            .filter(
                Q(rank__gte=0.2)
                | Q(trigram__gte=0.1)
                | Q(course_code__unaccent__trigram_similar=search_text)
            )
            .filter(id__in=ds)
            .order_by("-bs")
        )

        return qs

    def same_courses(self, user, course_list, university):

        n_id = [user.id]
        friends = Friend.objects.friends(user)
        blocked = Block.objects.blocking(user)

        if friends:
            for f in friends:
                n_id.append(int(f.id))
        if blocked:
            for b in blocked:
                n_id.append(int(b.id))

        courses = (
            self.get_queryset()
            .filter(
                course_code__in=course_list, profiles__university__iexact=university
            )
            .order_by("course_code", "course_university", "course_instructor")
            .distinct("course_code", "course_university", "course_instructor")
        )

        users = (
            Profile.objects.filter(courses__in=courses)
            .exclude(id__in=n_id)
            .order_by("username", "-date_joined")
            .distinct("username")
        )

        return users

    def instructor_average_voting(self, ins, ins_fn, university):

        avg = (
            self.get_queryset()
            .filter(
                course_instructor_fn__iexact=ins_fn,
                course_instructor=ins,
                course_university__unaccent=university,
            )
            .exclude(course_prof_difficulty=0)
            .annotate(as_float=Cast("course_prof_difficulty", FloatField()))
            .aggregate(Avg("as_float"))
        )

        if avg.get("as_float__avg"):
            return round(avg.get("as_float__avg"), 2)
        else:
            return -1


class CourseObjectManager(models.Manager):
    pass


class ProfessorsManager(models.Manager):
    def search(self, text, university=None, first_name=False):

        if first_name:
            search_vectors = SearchVector(
                "last_name", weight="C", config="english"
            ) + SearchVector("first_name", weight="A", config="english")
        else:
            search_vectors = SearchVector(
                "last_name", weight="A", config="english"
            ) + SearchVector("first_name", weight="A", config="english")

        search_query = SearchQuery(text, config="simple")

        search_rank = SearchRank(search_vectors, search_query)

        trigram_firstname = TrigramSimilarity("last_name", text)
        trigram_lastname = TrigramSimilarity("first_name", text)

        if university != None:
            qs = (
                self.get_queryset()
                .filter(university__unaccent__iexact=university)
                .annotate(
                    course_instructor_fn=F("first_name"),
                    course_instructor=F("last_name"),
                    course_university=F("university"),
                    trigram_firstname=trigram_firstname,
                    trigram_lastname=trigram_lastname,
                )
                .values(
                    "course_instructor_fn", "course_instructor", "course_university"
                )
                .filter(
                    Q(sv=search_query)
                    | Q(trigram_lastname__gte=0.2)
                    | Q(trigram_firstname__gte=0.3)
                )
                .annotate(rank=search_rank + trigram_firstname + trigram_lastname)
                .order_by("-rank")
            )
        else:
            qs = (
                self.get_queryset()
                .annotate(
                    course_instructor_fn=F("first_name"),
                    course_instructor=F("last_name"),
                    course_university=F("university"),
                    trigram_firstname=trigram_firstname,
                    trigram_lastname=trigram_lastname,
                )
                .values(
                    "course_instructor_fn", "course_instructor", "course_university"
                )
                .filter(
                    Q(sv=search_query)
                    | Q(trigram_lastname__gte=0.2)
                    | Q(trigram_firstname__gte=0.3)
                )
                .annotate(rank=search_rank + trigram_firstname + trigram_lastname)
                .order_by("-rank")
            )

        return qs


class Post(models.Model):
    title = models.CharField(max_length=100)
    guid_url = models.CharField(max_length=255, unique=True, null=True)
    content = models.TextField(validators=[MaxLengthValidator(2100)])
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)
    tags = TaggableManager(help_text="Tags", blank=True)
    likes = models.ManyToManyField(Profile, blank=True, related_name="post_likes")
    sv = pg_search.SearchVectorField(null=True)

    objects = PostManager()

    class Meta:
        indexes = [
            GinIndex(fields=["sv"], name="search_idx_post"),
        ]

    def __str__(self):
        return self.title

    def get_hashid(self):
        return hashids.encode(self.id)

    def get_absolute_url(self):
        return reverse("home:post-detail")

    def user_liked(self, request):
        return self.likes.filter(id=request.user.id).exists()

    def save(self, *args, **kwargs):
        self.guid_url = secrets.token_urlsafe(8)
        super(Post, self).save(*args, **kwargs)

    def comment_count(self):
        return self.comments.filter(post=self, reply=None).count()

    def image_count_as_list(self):
        c = self.images.count()
        return range(0, c)

    def get_created_on(self):
        now = timezone.now()
        diff = now - self.date_posted
        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds = diff.seconds
            return "Just now"
        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes = math.floor(diff.seconds / 60)
            return str(minutes) + "m"
        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours = math.floor(diff.seconds / 3600)
            return str(hours) + "h"
        if diff.days >= 1 and diff.days < 30:
            days = diff.days
            return str(days) + "d"
        if diff.days >= 30 and diff.days < 365:
            months = math.floor(diff.days / 7)
            return str(months) + "w"
        if diff.days >= 365:
            years = math.floor(diff.days / 365)
            return str(years) + "y"

    def has_image(self):
        if self.images.count() > 0:
            return True
        else:
            return False

    def edited(self):
        if (self.last_edited - self.date_posted).seconds > 1800:
            return True

    def get_edited_on(self):
        now = timezone.now()
        diff = now - self.last_edited
        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds = diff.seconds
            return "Just now"
        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes = math.floor(diff.seconds / 60)
            return str(minutes) + "m" + " ago "
        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours = math.floor(diff.seconds / 3600)
            return str(hours) + "h" + " ago "
        if diff.days >= 1 and diff.days < 30:
            days = diff.days
            return str(days) + "d" + " ago "
        if diff.days >= 30 and diff.days < 365:
            months = math.floor(diff.days / 7)
            return str(months) + "w" + " ago "
        if diff.days >= 365:
            years = math.floor(diff.days / 365)
            return str(years) + "y" + " ago "

    def hot(self):

        comments = self.comments.count()
        likes = self.likes.count()
        date = self.last_edited

        s = score(comments, likes)
        z = log(max(abs(s), 1), 10)
        y = 1 if s > 0 else -1 if s < 0 else 0
        seconds = epoch_seconds(date) - 1134028003
        return round(y * z + seconds / 45000, 7)

    def top(self):

        comments = self.comments.count()
        likes = self.likes.count()

        return top_score_posts(likes, comments)

    def get_comments(self, ids):

        comments = self.comments.select_related("name").order_by("-created_on")


def image_create_uuid_p_u(instance, filename):
    return "/".join(["post_images", str(uuid.uuid4().hex + ".png")])


class Images(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="images")
    image = models.FileField(
        upload_to=upload_to_uuid("media/post_images/"), verbose_name="Image"
    )
    date_added = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        if self.pk is None:
            MAX_WIDTH = 1080
            MAX_HEIGHT = 1350
            img = Image.open(self.image)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            exif = None
            if "exif" in img.info:
                exif = img.info["exif"]
            ratio = min(MAX_WIDTH / img.size[0], MAX_HEIGHT / img.size[1])
            if img.size[0] > MAX_WIDTH or img.size[1] > MAX_HEIGHT:
                img = img.resize(
                    (int(img.size[0] * ratio), int(img.size[1] * ratio)),
                    PIL.Image.ANTIALIAS,
                )
            else:
                img = img.resize((img.size[0], img.size[1]), PIL.Image.ANTIALIAS)
            output = io.BytesIO()
            if exif:
                img.save(output, format="JPEG", exif=exif, quality=90)
            else:
                img.save(output, format="JPEG", quality=90)
            output.seek(0)
            self.image = InMemoryUploadedFile(
                output,
                "ImageField",
                "%s.jpg" % self.image.name,
                "image/jpeg",
                output.getbuffer().nbytes,
                None,
            )
            super(Images, self).save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.ForeignKey(Profile, on_delete=models.CASCADE)
    body = models.TextField(validators=[MaxLengthValidator(350)])
    created_on = models.DateTimeField(auto_now_add=True)
    reply = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, related_name="replies"
    )
    likes = models.ManyToManyField(Profile, blank=True, related_name="comment_likes")

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return "Comment {} by {}".format(self.body, self.name)

    @property
    def is_reply(self):
        return self.reply_id is not None

    def likes_count(self):
        return self.likes.count()

    def get_hashid(self):
        return hashids.encode(self.id)

    def get_created_on(self):
        now = timezone.now()
        diff = now - self.created_on
        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds = diff.seconds
            return str(seconds) + " s"
        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes = math.floor(diff.seconds / 60)
            return str(minutes) + "m"
        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours = math.floor(diff.seconds / 3600)
            return str(hours) + "h"
        if diff.days >= 1 and diff.days < 30:
            days = diff.days
            return str(days) + "d"
        if diff.days >= 30 and diff.days < 365:
            months = math.floor(diff.days / 7)
            return str(months) + "w"
        if diff.days >= 365:
            years = math.floor(diff.days / 365)
            return str(years) + "y"

    def get_uuid(self):
        return str(uuid.uuid4())


class Review(models.Model):
    class Interesting(models.TextChoices):
        INTERESTING = "1", "Interesting"
        RELATIVELY = "2", "Relatively Interesting"
        NOT = "3", "Not Interesting"
        NO_OPINION = "4", "No opinion"

    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    body = models.TextField(validators=[MaxLengthValidator(400)])
    created_on = models.DateTimeField(auto_now_add=True)
    is_anonymous = models.BooleanField(default=False, blank=False)
    likes = models.ManyToManyField(Profile, blank=True, related_name="review_likes")
    dislikes = models.ManyToManyField(
        Profile, blank=True, related_name="review_dislikes"
    )
    review_interest = models.CharField(
        max_length=2, choices=Interesting.choices, default=Interesting.NO_OPINION
    )
    year = models.IntegerField(
        ("year"),
        validators=[
            MinValueValidator(1984),
            MaxValueValidator(max_value_current_year()),
        ],
        null=True,
    )

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return "Review {} by {}".format(self.body, self.author.get_username)

    def get_hashid(self):
        return hashids.encode(self.id)

    def get_author(self):

        if self.is_anonymous:
            return "Anonymous Student"
        else:
            return self.author.get_full_name()

    def get_interest(self):
        interest = {
            "1": "Interesting",
            "2": "Relatively Interesting",
            "3": "Not Interesting",
            "4": "No Opinion",
        }
        return interest[self.review_interest]

    def get_created_on(self):
        now = timezone.now()
        diff = now - self.created_on
        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds = diff.seconds
            return "Just now"
        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes = math.floor(diff.seconds / 60)
            return str(minutes) + "m"
        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours = math.floor(diff.seconds / 3600)
            return str(hours) + "h"
        if diff.days >= 1 and diff.days < 30:
            days = diff.days
            return str(days) + "d"
        if diff.days >= 30 and diff.days < 365:
            months = math.floor(diff.days / 7)
            return str(months) + "w"
        if diff.days >= 365:
            years = math.floor(diff.days / 365)
            return str(years) + "y"

    def get_course_prof(self):
        return (
            Course.objects.get(course_reviews__id=self.id).course_instructor_fn
            + " "
            + Course.objects.get(course_reviews__id=self.id).course_instructor
        )

    def get_course_yr(self):
        return Course.objects.get(course_reviews__id=self.id).course_year

    def get_course_sm(self):
        return Course.objects.get(course_reviews__id=self.id).sem()


class Course(models.Model):
    class Difficulty(models.TextChoices):
        NONE = "0", "TBD"
        EASY = "4", "Easy"
        MEDIUM = "3", "Medium"
        HARD = "2", "Hard"
        FAILED = "1", "Failed"

    class ProfDifficulty(models.TextChoices):
        NONE = "0", "TBD"
        EASY = "4", "Easy"
        MEDIUM = "3", "Medium"
        HARD = "2", "Hard"
        FAILED = "1", "Failed"

    course_code = models.CharField(max_length=100)
    course_university = models.CharField(max_length=100)
    course_university_slug = models.SlugField(max_length=250, null=True, blank=True)
    course_instructor_slug = models.SlugField(max_length=250, null=True, blank=True)
    course_instructor = models.CharField(max_length=100)
    course_instructor_fn = models.CharField(max_length=100)
    course_year = models.IntegerField(
        ("year"),
        validators=[
            MinValueValidator(1984),
            MaxValueValidator(max_value_current_year()),
        ],
    )
    course_likes = models.ManyToManyField(
        Profile, blank=True, related_name="course_likes"
    )
    course_dislikes = models.ManyToManyField(
        Profile, blank=True, related_name="course_dislikes"
    )
    course_reviews = models.ManyToManyField(
        Review, blank=True, related_name="course_reviews"
    )
    course_difficulty = models.CharField(
        max_length=2, choices=Difficulty.choices, default=Difficulty.NONE, blank=True
    )
    course_prof_difficulty = models.CharField(
        max_length=2,
        choices=ProfDifficulty.choices,
        default=ProfDifficulty.NONE,
        blank=True,
    )

    sv = pg_search.SearchVectorField(null=True)

    objects = CourseManager()

    class Meta:
        indexes = [
            GinIndex(fields=["sv"], name="search_idx_course"),
        ]

    def __str__(self):
        return self.course_code

    def save(self, *args, **kwargs):
        self.course_code = self.course_code.upper().replace(" ", "")
        self.course_instructor = self.course_instructor.strip().lower()
        self.course_instructor_fn = self.course_instructor_fn.strip().lower()
        self.course_instructor_slug = "-".join(
            (
                slugify(self.course_instructor_fn.strip().lower()),
                slugify(self.course_instructor.strip().lower()),
            )
        )
        self.course_university_slug = slugify(self.course_university.strip().lower())
        super(Course, self).save(*args, **kwargs)

    def get_hashid(self):
        return hashids.encode(self.id)

    def get_user_count(self):
        count = (
            Profile.objects.select_related('courses').filter(
                courses__course_code=self.course_code,
                courses__course_university__iexact=self.course_university,
            )
            .distinct("username")
            .count()
        )
        return count

    def get_user_count_ins(self):
        count = (
            Profile.objects.select_related('courses').filter(
                courses__course_instructor_fn__iexact=self.course_instructor_fn,
                courses__course_instructor__iexact=self.course_instructor,
                courses__course_code=self.course_code,
                courses__course_university__iexact=self.course_university,
            )
            .distinct("username")
            .count()
        )
        return count

    def average_voting(self):

        # removed course instructor filtration from average voting. Apply distinct user filter?
        # distinct filter user -> users vote will count only for one course object!
        total_likes = Course.course_likes.through.objects.filter(
            course__course_code=self.course_code,
            course__course_university__iexact=self.course_university,
        ).count()
        total_dislikes = Course.course_dislikes.through.objects.filter(
            course__course_code=self.course_code,
            course__course_university__iexact=self.course_university,
        ).count()
        t = total_likes - total_dislikes
        if t == 0:
            return "Rate"
        t = float("{:.3g}".format(t))
        magnitude = 0
        while abs(t) >= 1000:
            magnitude += 1
            t /= 1000.0
        return "{}{}".format(
            "{:f}".format(t).rstrip("0").rstrip("."),
            ["", "K", "M", "B", "T"][magnitude],
        )

    def complexity_btn(self):
        r_dic = {
            None: "None",
            "Easy": "success",
            "Medium": "warning",
            "Hard": "danger",
            "Most Failed": "dark",
        }
        return r_dic[self.average_complexity()]

    def complexity_btn_ins(self):
        r_dic = {
            None: "None",
            "Easy": "success",
            "Medium": "warning",
            "Hard": "danger",
            "Most Failed": "dark",
        }
        return r_dic[self.average_complexity_ins()]

    def average_complexity(self):
        r_dic = {
            4: "Easy",
            3: "Medium",
            2: "Hard",
            1: "Most Failed",
        }
        try:
            avg_cplx = cache.get(
                "courses_avg_cplx__{}__{}".format(
                    self.course_code.replace(" ", ""), self.course_university_slug
                )
            )
            if avg_cplx == None:
                avg = list(
                    Course.objects.select_related('profiles').exclude(course_difficulty=0)
                    .filter(
                        course_code=self.course_code,
                        course_university__iexact=self.course_university,
                    )
                    .values("course_difficulty")
                    .annotate(count=Count("profiles__id"))
                    .order_by("course_difficulty")
                )

                total_users = sum_ratings = 0
                for el in avg:
                    total_users += el["count"]
                    sum_ratings += int(el["course_difficulty"]) * el["count"]
                avg_cplx = r_dic[round(sum_ratings / total_users)]
                cache.set(
                    "courses_avg_cplx__{}__{}".format(
                        self.course_code.replace(" ", ""), self.course_university_slug
                    ),
                    avg_cplx,
                    7200,
                )
            return avg_cplx
        except Exception as e:
            print(e.__class__)
            return None

    def average_complexity_ins(self):
        r_dic = {
            4: "Easy",
            3: "Medium",
            2: "Hard",
            1: "Most Failed",
        }  # need to get profiles that have the ratings not the course
        try:
            avg_cplx = cache.get(
                "courses_avg_cplx__{}__{}__{}".format(
                    self.course_code.replace(" ", ""),
                    self.course_university_slug,
                    self.course_instructor_slug,
                )
            )
            if avg_cplx == None:
                avg = list(
                    Course.objects.select_related('profiles').exclude(course_difficulty=0)
                    .filter(
                        course_code=self.course_code,
                        course_university__iexact=self.course_university,
                        course_instructor__iexact=self.course_instructor,
                        course_instructor_fn__iexact=self.course_instructor_fn,
                    )
                    .exclude(course_difficulty=0)
                    .values("course_difficulty")
                    .annotate(count=Count("profiles__id"))
                    .order_by("course_difficulty")
                )

                total_users = sum_ratings = 0
                for el in avg:
                    total_users += el["count"]
                    sum_ratings += int(el["course_difficulty"]) * el["count"]
                avg_cplx = r_dic[round(sum_ratings / total_users)]
                cache.set(
                    "courses_avg_cplx__{}__{}__{}".format(
                        self.course_code.replace(" ", ""),
                        self.course_university_slug,
                        self.course_instructor_slug,
                    ),
                    avg_cplx,
                    10600,
                )
            return avg_cplx
        except Exception as e:
            print(e.__class__)
            return None

    def user_complexity(self):
        r_dic = {0: "none", 4: "easy", 3: "medium", 2: "hard", 1: "a failure"}
        return r_dic[int(self.course_difficulty)]

    def user_complexity_btn(self):
        r_dic = {0: "None", 4: "Easy", 3: "Medium", 2: "Hard", 1: "Most Failed"}
        return r_dic[int(self.course_difficulty)]

    def is_liked(self, user):
        return Course.course_likes.through.objects.filter(
            course__course_code=self.course_code,
            course__course_university__iexact=self.course_university,
            profile_id=user.id,
        ).exists()

    def not_liked(self, user):
        return Course.course_dislikes.through.objects.filter(
            course__course_code=self.course_code,
            course__course_university__iexact=self.course_university,
            profile_id=user.id,
        ).exists()

    def get_reviews(self, order=None):

        order_by = {
            None: "-created_on",
            "cy": "-year",
            "latest": "-created_on",
        }

        try:
            return Review.objects.select_related('author').filter(
                course_reviews__course_code=self.course_code,
                course_reviews__course_instructor__iexact=self.course_instructor,
                course_reviews__course_instructor_fn__iexact=self.course_instructor_fn,
                course_reviews__course_university__iexact=self.course_university,
            ).order_by(order_by[order])
        except Exception as e:
            print(e)
            return Review.objects.select_related('author').filter(
                course_reviews__course_code=self.course_code,
                course_reviews__course_instructor__iexact=self.course_instructor,
                course_reviews__course_instructor_fn__iexact=self.course_instructor_fn,
                course_reviews__course_university__iexact=self.course_university,
            ).order_by("-created_on")

    def get_reviews_all(self, order=None):

        order_by = {
            None: "-created_on",
            "cy": "-year",
        }
        
        cache_index = {
            None: "",
            "latest":"",
            "cy": "__yr",
        }

        try:          
            result = cache.get("courses_reviews__{}__{}__all_{}".format(self.course_code, self.course_university_slug, cache_index[order]))
            if result == None:
                if order == "cy":
                    qs = Review.objects.select_related('author').filter(
                        course_reviews__course_code=self.course_code,
                        course_reviews__course_university__iexact=self.course_university,
                    ).order_by(
                        "course_reviews__course_instructor","course_reviews__course_instructor_fn","-year", "-created_on",
                    ).annotate(
                        instructor_first_name=F('course_reviews__course_instructor_fn'),
                        instructor_last_name=F('course_reviews__course_instructor'),
                    )
                else:
                    qs = Review.objects.select_related('author').filter(
                        course_reviews__course_code=self.course_code,
                        course_reviews__course_university__iexact=self.course_university,
                    ).order_by(
                        "course_reviews__course_instructor","course_reviews__course_instructor_fn", "-created_on",
                    ).annotate(
                        instructor_first_name=F('course_reviews__course_instructor_fn'),
                        instructor_last_name=F('course_reviews__course_instructor'),
                    )
                result = {
                    k: list(vs)
                    for k, vs in groupby(qs, attrgetter('instructor_last_name','instructor_first_name'))
                }
                cache.set("courses_reviews__{}__{}__all{}".format(self.course_code, self.course_university_slug, cache_index[order]), result)
            return result      
        except Exception as e:
            print(e)
            return []
        
        except Exception as e:
            print(e)
            return Review.objects.select_related('author').filter(
                course_reviews__course_code=self.course_code,
                course_reviews__course_university__iexact=self.course_university,
            ).order_by("-created_on")

    def reviews_count(self):
        
        count = cache.get("courses_review__count__{}_{}_{}".format(self.course_university_slug, self.course_code, self.course_instructor_slug))
        if count == None:
            count = Course.course_reviews.through.objects.filter(
                course__course_code=self.course_code,
                course__course_university__iexact=self.course_university,
                course__course_instructor_fn__iexact=self.course_instructor_fn,
                course__course_instructor__iexact=self.course_instructor,
            ).count()
            cache.set("courses_review__count__{}_{}_{}".format(self.course_university_slug, self.course_code, self.course_instructor_slug), count)
        return count
    
    def reviews_all_count(self):

        count = cache.get("courses_review__count__{}_{}__all".format(self.course_university_slug, self.course_code))
        if count == None:
            count = Course.course_reviews.through.objects.filter(
                course__course_code=self.course_code,
                course__course_university__iexact=self.course_university,
            ).count()
            cache.set("courses_review__count__{}_{}__all".format(self.course_university_slug, self.course_code), count)
        return count


class Buzz(models.Model):
    nickname = models.CharField(max_length=30, blank=True, null=True)
    title = models.CharField(max_length=90)
    guid_url = models.CharField(max_length=255, unique=True)
    content = models.TextField(validators=[MaxLengthValidator(550)])
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)
    expiry = models.DateTimeField(blank=True, null=True)
    tags = TaggableManager(help_text="Tags", blank=True)
    likes = models.ManyToManyField(Profile, blank=True, related_name="likes")
    dislikes = models.ManyToManyField(Profile, blank=True, related_name="dilikes")
    wots = models.ManyToManyField(Profile, blank=True, related_name="wots")
    shares = models.ManyToManyField(Profile, blank=True, related_name="shares")
    sv = pg_search.SearchVectorField(null=True)

    objects = BuzzManager()

    class Meta:
        indexes = [
            GinIndex(fields=["sv"], name="search_idx_buzz"),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.guid_url = secrets.token_urlsafe(12)
        super(Buzz, self).save(*args, **kwargs)

    def get_hashid(self):
        return hashids.encode(self.id)

    def get_created_on(self):
        now = timezone.now()
        diff = now - self.date_posted
        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds = diff.seconds
            return "Just now"
        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes = math.floor(diff.seconds / 60)
            return str(minutes) + "m"
        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours = math.floor(diff.seconds / 3600)
            return str(hours) + "h"
        if diff.days >= 1 and diff.days < 30:
            days = diff.days
            return str(days) + "d"
        if diff.days >= 30 and diff.days < 365:
            months = math.floor(diff.days / 7)
            return str(months) + "w"
        if diff.days >= 365:
            years = math.floor(diff.days / 365)
            return str(years) + "y"

    def get_expiry(self):
        if self.expiry is not None:
            now = timezone.now()
            if self.expiry > now:
                diff = self.expiry - now
                if diff.seconds >= 3600 and diff.days < 1:
                    hours = math.floor(diff.seconds / 3600)
                    return "expirying in " + str(hours) + "h"
                if diff.days >= 1 and diff.days < 30:
                    days = diff.days
                    return "expirying in " + str(days) + "d"
            else:
                diff = now - self.expiry
                if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
                    seconds = diff.seconds
                    return "Just expired"
                if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
                    minutes = math.floor(diff.seconds / 60)
                    return "expired " + str(minutes) + "m" + " ago"
                if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
                    hours = math.floor(diff.seconds / 3600)
                    return "expired " + str(hours) + "h" + " ago"
                if diff.days >= 1 and diff.days < 30:
                    days = diff.days
                    return "expired " + str(days) + "d" + " ago"
                if diff.days >= 30 and diff.days < 365:
                    months = math.floor(diff.days / 7)
                    return "expired " + str(months) + "w" + " ago"
                if diff.days >= 365:
                    years = math.floor(diff.days / 365)
                    return "expired " + str(years) + "y" + " ago"

    def hot(self):

        comments = self.breplies.count()
        likes = self.likes.count()
        dislikes = self.dislikes.count()
        wots = self.wots.count()
        date = self.last_edited

        return hot_buzz(likes, dislikes, wots, comments, date)

    def top(self):

        comments = self.breplies.count()
        likes = self.likes.count()
        dislikes = self.dislikes.count()
        wots = self.wots.count()

        return top_buzz(likes, dislikes, wots, comments)


class BuzzReply(models.Model):

    buzz = models.ForeignKey(Buzz, on_delete=models.CASCADE, related_name="breplies")
    reply_nickname = models.CharField(max_length=30, blank=True, null=True)
    reply_content = models.TextField(validators=[MaxLengthValidator(180)])
    reply_author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date_replied = models.DateTimeField(auto_now_add=True)
    reply_likes = models.ManyToManyField(Profile, blank=True, related_name="rlikes")
    reply_dislikes = models.ManyToManyField(
        Profile, blank=True, related_name="rdislikes"
    )

    def __str__(self):
        return self.reply_nickname

    def get_hashid(self):
        return hashids.encode(self.id)

    def get_created_on(self):
        now = timezone.now()
        diff = now - self.date_replied
        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds = diff.seconds
            return "Just now"
        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes = math.floor(diff.seconds / 60)
            return str(minutes) + "m"
        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours = math.floor(diff.seconds / 3600)
            return str(hours) + "h"
        if diff.days >= 1 and diff.days < 30:
            days = diff.days
            return str(days) + "d"
        if diff.days >= 30 and diff.days < 365:
            months = math.floor(diff.days / 7)
            return str(months) + "w"
        if diff.days >= 365:
            years = math.floor(diff.days / 365)
            return str(years) + "y"


class Blog(models.Model):

    title = models.CharField(max_length=200)
    guid_url = models.CharField(max_length=255, unique=True)
    content = RichTextUploadingField(blank=True, null=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)
    tags = TaggableManager(help_text="Tags", blank=True)
    slug = models.SlugField(null=True, blank=True)
    likes = models.ManyToManyField(Profile, blank=True, related_name="blog_likes")
    sv = pg_search.SearchVectorField(null=True)

    objects = BlogManager()

    class Meta:
        indexes = [
            GinIndex(fields=["sv"], name="search_idx_blog"),
        ]

    def save(self, *args, **kwargs):
        self.guid_url = secrets.token_urlsafe(6)
        self.title = self.title.strip()
        self.slug = slugify(self.title.strip().lower())
        super(Blog, self).save(*args, **kwargs)

    def get_hashid(self):
        return hashids.encode(self.id)

    def get_readtime(self):
        result = readtime.of_text(str(self.content))
        result = round(result.seconds / 60)
        if result <= 1:
            return "1 min"
        else:
            return str(result) + " min"


class BlogReply(models.Model):

    blog = models.ForeignKey(
        Blog, on_delete=models.CASCADE, related_name="blog_replies"
    )
    content = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date_replied = models.DateTimeField(auto_now_add=True)
    reply_likes = models.ManyToManyField(Profile, blank=True, related_name="brlikes")

    def __str__(self):
        return self.reply_nickname

    def get_hashid(self):
        return hashids.encode(self.id)

    def get_created_on(self):
        now = timezone.now()
        diff = now - self.date_replied
        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds = diff.seconds
            return "Just now"
        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes = math.floor(diff.seconds / 60)
            return str(minutes) + "m"
        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours = math.floor(diff.seconds / 3600)
            return str(hours) + "h"
        if diff.days >= 1 and diff.days < 30:
            days = diff.days
            return str(days) + "d"
        if diff.days >= 30 and diff.days < 365:
            months = math.floor(diff.days / 7)
            return str(months) + "w"
        if diff.days >= 365:
            years = math.floor(diff.days / 365)
            return str(years) + "y"


class CourseList(models.Model):

    creator = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="course_lists"
    )
    title = models.CharField(max_length=1000)
    created_on = models.DateTimeField(auto_now_add=True)
    year = models.IntegerField(
        ("year"),
        validators=[
            MinValueValidator(1984),
            MaxValueValidator(max_value_current_year()),
        ],
        blank=True,
    )
    guid = models.CharField(max_length=255, unique=True, null=True)

    def __str__(self):
        return self.title

    def get_hashid(self):
        return hashid_list.encode(self.id)

    def save(self, *args, **kwargs):
        self.guid = secrets.token_urlsafe(16)
        super(CourseList, self).save(*args, **kwargs)


class CourseListObjects(models.Model):

    parent_list = models.ForeignKey(
        CourseList, on_delete=models.CASCADE, related_name="added_courses"
    )
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    course_code = models.CharField(max_length=20)
    course_university = models.CharField(max_length=100)
    course_instructor = models.CharField(max_length=100, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.parent_list.title + "-" + self.course_code

    def get_created_on(self):
        now = timezone.now().replace(tzinfo=timezone.utc).astimezone(tz=None)

        diff = now - self.created_on.replace(tzinfo=timezone.utc).astimezone(tz=None)

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds = diff.seconds
            return "Just now"
        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes = math.floor(diff.seconds / 60)
            return str(minutes) + "m ago"
        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours = math.floor(diff.seconds / 3600)
            return str(hours) + "h ago"
        if diff.days >= 1 and diff.days < 30:
            days = diff.days
            return str(days) + "d ago"
        if diff.days >= 30 and diff.days < 365:
            months = math.floor(diff.days / 7)
            return str(months) + "w ago"
        if diff.days >= 365:
            years = math.floor(diff.days / 365)
            return str(years) + "y ago"

    def get_hashid(self):
        return hashids.encode(self.id)


class CourseObject(models.Model):

    code = models.CharField(max_length=100)
    university = models.CharField(max_length=255)
    university_slug = models.SlugField(max_length=255, null=True, blank=True)
    enrolled = models.ManyToManyField(
        Profile, blank=True, related_name="enrolled_students"
    )
    # obj_likes = models.ManyToManyField(
    #     Profile, blank=True, related_name="course_obj_likes"
    # )
    # obj_dislikes = models.ManyToManyField(
    #     Profile, blank=True, related_name="course_obj_dislikes"
    # )

    def __str__(self):
        return self.course_code

    sv = pg_search.SearchVectorField(null=True)

    objects = CourseObjectManager()

    class Meta:
        indexes = [
            GinIndex(fields=["sv"], name="search_idx_course_obj"),
        ]

    def save(self, *args, **kwargs):
        self.code = self.code.upper().replace(" ", "").strip()
        self.university_slug = slugify(self.university.strip().lower())
        super(CourseObject, self).save(*args, **kwargs)

class Professors(models.Model):

    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    university = models.CharField(max_length=255, null=False)
    courses = models.ManyToManyField(CourseObject, related_name="instructor_courses")
    university_slug = models.SlugField(max_length=250, null=True, blank=True)
    name_slug = models.SlugField(max_length=250, null=True, blank=True)
    ratings = models.DecimalField(max_digits=15, decimal_places=6, null=True)

    sv = pg_search.SearchVectorField(null=True)

    objects = ProfessorsManager()

    class Meta:
        indexes = [
            GinIndex(fields=["sv"], name="search_idx_professors"),
        ]

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.strip().lower()
        self.last_name = self.last_name.strip().lower()
        self.university_slug = slugify(self.university.strip().lower())
        self.name_slug = "-".join(
            (
                slugify(self.first_name.strip().lower()),
                slugify(self.last_name.strip().lower()),
            )
        )
        super(Professors, self).save(*args, **kwargs)

    def get_instructor_page_url(self):

        try:
            if self.name_slug and self.university_slug:
                return reverse(
                    "home:course-instructor",
                    kwargs={"par1": self.university_slug, "par2": self.name_slug},
                )
            return "#"
        except Exception as e:
            print(e)
            return "#"

    def get_student_count(self):

        try:
            count = (
                Profile.objects.filter(
                    courses__course_instructor_fn__iexact=self.first_name,
                    courses__course_instructor__iexact=self.last_name,
                    courses__course_university__iexact=self.university,
                )
                .distinct("username")
                .count()
            )
            return count
        except Exception as e:
            print(e)
            return 0

    def add_to_courses(self, course):

        try:
            if not self.courses.filter(
                course_code=course.code,
                course_university=course.university,
            ).exists():
                self.courses.add(course)
                self.save()
        except Exception as e:
            print(e)
            print(e.__class__)


