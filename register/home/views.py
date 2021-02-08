from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views import View
from django.utils import timezone
from django.db.models import Q, F, Count, Avg, FloatField, Max, Min, Case, When
from hashids import Hashids
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
    RedirectView,
)
from django.forms import modelformset_factory
from .models import (
    Post,
    Comment,
    Images,
    Course,
    Review,
    Buzz,
    BuzzReply,
    Blog,
    BlogReply,
    CourseList,
    CourseListObjects,
    Professors,
    CourseObject,
)
from main.models import Profile, SearchLog, BookmarkPost
from .forms import (
    PostForm,
    CommentForm,
    CourseForm,
    CourseEditForm,
    ImageForm,
    ReviewForm,
    BuzzForm,
    BuzzReplyForm,
    BlogForm,
    BlogReplyForm,
    CourseListForm,
    CourseListObjectsForm,
)
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .post_guid import uuid2slug, slug2uuid
from django.urls import reverse
import datetime
from datetime import timedelta
from django.db.models.functions import Now
from django.utils.timezone import make_aware
from dal import autocomplete
from taggit.models import Tag
from friendship.models import Friend, Follow, Block, FriendshipRequest
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.core.cache import cache
from django.contrib.postgres.search import (
    SearchQuery,
    SearchRank,
    SearchVector,
    TrigramSimilarity,
)
from notifications.signals import notify
import json
from home.algo import get_uni_info, get_similar_university
from itertools import chain, groupby
from operator import attrgetter
from home.templatetags.ibuilder import num_format
from django.contrib.admin.options import get_content_type_for_model
from django.contrib.contenttypes.models import ContentType
from home.forms import current_year
from home.tasks import (
    async_send_mention_notifications,
    async_delete_mention_notifications,
    async_update_mention_notifications,
    add_user_to_course,
    remove_user_from_course,
    add_course_to_prof,
    user_get_or_set_top_school_courses,
    set_course_objects_top_courses,
)
from django.templatetags.static import static
from django.contrib.staticfiles import finders
from home.redis_handlers import update_course_reviews_cache, adjust_course_avg_hash
from assets.assets import UNI_LIST
from django.core import serializers
from .serializers import CommentSerializer

hashids = Hashids(salt="v2ga hoei232q3r prb23lqep weprhza9", min_length=8)

hashid_list = Hashids(salt="e5896e mqwefv0t mvSOUH b90 NS0ds90", min_length=16)

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)

# main page that user see's the hope page
@login_required
def home(request):

    try:
        no_friends_and_university = no_friends_only = discover_students = False
        no_post_message = ""
        if len(request.user.university) < 1:
            request.session["no_university"] = True
        words = posts = []  # return none if paginator failed to return
        friends = Friend.objects.friends(request.user)
        try:
            if (len(request.user.university) < 1) and (len(friends) < 1):
                no_friends_and_university = True
                no_post_message = "Welcome to JoinCampus!"
        except Exception as e:
            print(e.__class__)
            print(e)

        """ get a list of users that user has blocked and save it to request.session """
        try:
            if request.session.get("blockers") == None:
                blockers_list = Block.objects.blocked(request.user)
                request.session["blockers"] = [u.id for u in blockers_list]
        except Exception as e:
            print(e)
            request.session["blockers"] = []

        posts_list = (
            Post.objects.select_related("author")
            .filter(Q(author__in=friends) | Q(author=request.user))
            .order_by("-last_edited")
        )

        try:
            if posts_list.count() < 1:
                if len(request.user.university) > 1:
                    uni = request.user.university
                    posts_list = cache.get(
                        uni.replace(" ", "") + "_latest_university_posts"
                    )
                    if posts_list == None:
                        posts_list = (
                            Post.objects.select_related("author")
                            .filter(Q(author__university=request.user.university))
                            .order_by("-last_edited")
                        )
                        cache.set(
                            uni.replace(" ", "") + "_latest_university_posts",
                            posts_list,
                            7200,
                        )
                    no_post_message = "Latest posts at " + request.user.university
                    if posts_list.count() < 1:
                        discover_students = True
                else:  # the user may or may not have any friends however, university is still not set
                    no_friends_and_university = (
                        True  # show same message as user with no friends and school set
                    )
                    no_post_message = "Find more students to see their posts"  # display additional message meaning user probably had no friends or friends haven't posted
        except Exception as e:
            print(e.__class__)
            print(e)
            posts_list = []  # just return an empty posts list
        """ get hot words and tags related to posts form tags """
        tags = cache.get("tt_post")
        top_words = cache.get("trending_words_posts")
        if top_words:
            words = top_words["phrases"]

        """ @param is_home is set to True """
        """ home.html is used in other functions, is_home changes the view """
        is_home = True
        page = request.GET.get("page", 1)
        paginator = Paginator(posts_list, 10)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context = {
            "posts": posts,
            "is_home": is_home,
            "tags": tags,
            "words": words,
            "home_active": "-active",
            "discover_students": discover_students,
            "no_post_message": no_post_message,
            "no_friends_and_university": no_friends_and_university,
        }
        return render(request, "home/homepage/home.html", context)
    except Exception as e:
        print(e.__class__)
        print(e)
        context = {
            "posts": [],
            "is_home": True,
            "home_active": "-active",
        }
        return render(request, "home/homepage/home.html", context)


@login_required
def users_posts(request):

    order = request.GET.get("o", "latest")
    if order == "latest":
        posts_list = request.user.post_set.order_by("-last_edited")
    elif order == "oldest":
        posts_list = request.user.post_set.order_by("last_edited")
    elif order == "title":
        posts_list = request.user.post_set.order_by("title")
    elif order == "likes":
        posts_list = request.user.post_set.annotate(like_count=Count("likes")).order_by(
            "-like_count"
        )
    elif order == "comments":
        posts_list = request.user.post_set.annotate(
            comment_count=Count("comments")
        ).order_by("-comment_count")
    else:
        posts_list = request.user.post_set.order_by("-last_edited")

    page = request.GET.get("page", 1)
    paginator = Paginator(posts_list, 10)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {"posts": posts, "post_active": "-active", "o": order}
    return render(request, "home/homepage/user_byyou.html", context)


@login_required
def users_blogs(request):

    order = request.GET.get("o", "latest")
    if order == "latest":
        blogs_list = request.user.blog_set.order_by("-last_edited")
    elif order == "oldest":
        blogs_list = request.user.blog_set.order_by("last_edited")
    elif order == "title":
        blogs_list = request.user.blog_set.order_by("title")
    elif order == "likes":
        blogs_list = request.user.blog_set.annotate(like_count=Count("likes")).order_by(
            "-like_count"
        )
    elif order == "replies":
        blogs_list = request.user.blog_set.annotate(
            reply_count=Count("blog_replies")
        ).order_by("-reply_count")
    else:
        blogs_list = request.user.blog_set.order_by("-last_edited")

    page = request.GET.get("page", 1)
    paginator = Paginator(blogs_list, 10)
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)

    context = {"blogs": blogs, "blog_active": "-active", "o": order}
    return render(request, "home/homepage/user_byyou.html", context)


@login_required
def hot_posts(request):

    blockers_id = words = post_list_ids = posts_list = []

    """ @param preserved keeps the order of the hot posts """
    posts_list_ids = cache.get("hot_posts")
    blockers_id = request.session.get("blockers")

    if posts_list_ids:
        preserved = Case(
            *[When(pk=pk, then=pos) for pos, pk in enumerate(posts_list_ids)]
        )
        if request.user.university:
            posts_list = (
                Post.objects.select_related("author")
                .annotate(
                    relevancy=Count(
                        Case(
                            When(author__university=request.user.university, then=None)
                        )
                    )
                )
                .filter(id__in=posts_list_ids)
                .exclude(author__id__in=blockers_id)
                .order_by(-preserved)
            )
        else:
            posts_list = (
                Post.objects.select_related("author")
                .filter(id__in=posts_list_ids)
                .exclude(author__id__in=blockers_id)
                .order_by(-preserved)
            )

    """ get hot words and tags related to posts form tags """
    tags = cache.get("tt_post")
    top_words = cache.get("trending_words_posts")

    if top_words:
        words = top_words["phrases"]
        words = words + top_words["common_words"]

    page = request.GET.get("page", 1)
    paginator = Paginator(posts_list, 10)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        "posts": posts,
        "hot_active": "-active",
        "tags": tags,
        "words": words,
        "is_home": True,
    }
    return render(request, "home/homepage/home.html", context)


@login_required
def top_posts(request):

    blockers_id = words = posts_list_ids = posts_list = []

    """ @param preserved keeps the order of the hot posts """
    posts_list_ids = cache.get("top_posts")
    blockers_id = request.session.get("blockers")

    if posts_list_ids:
        preserved = Case(
            *[When(pk=pk, then=pos) for pos, pk in enumerate(posts_list_ids)]
        )
        if request.user.university:
            posts_list = (
                Post.objects.select_related("author")
                .annotate(
                    relevancy=Count(
                        Case(
                            When(author__university=request.user.university, then=None)
                        )
                    )
                )
                .filter(id__in=posts_list_ids)
                .exclude(author__id__in=blockers_id)
                .order_by(-preserved)
            )
        else:
            posts_list = (
                Post.objects.select_related("author")
                .filter(id__in=posts_list_ids)
                .exclude(author__id__in=blockers_id)
                .order_by(-preserved)
            )

    """ get hot words and tags related to posts form tags """
    tags = cache.get("tt_post")
    top_words = cache.get("trending_words_posts")
    if top_words:
        words = top_words["phrases"]
        words = words + top_words["common_words"]

    page = request.GET.get("page", 1)
    paginator = Paginator(posts_list, 10)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        "posts": posts,
        "top_active": "-active",
        "tags": tags,
        "words": words,
        "is_home": True,
    }
    return render(request, "home/homepage/home.html", context)


@login_required
def uni_posts(request):

    words = []
    posts = None

    u = request.user.university
    t = u.lower().replace(" ", "_") + "_post"

    posts_list = cache.get(t)

    blockers_id = request.session.get("blockers")

    if posts_list:
        posts_list = posts_list.exclude(author__id__in=blockers_id)
        page = request.GET.get("page", 1)
        paginator = Paginator(posts_list, 10)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

    """ get hot words and tags related to posts form tags """
    tags = cache.get("tt_post")
    top_words = cache.get("trending_words_posts")
    if top_words:
        words = top_words["phrases"]
        words = words + top_words["common_words"]

    context = {
        "posts": posts,
        "uni_active": "-active",
        "tags": tags,
        "words": words,
        "is_home": True,
    }

    return render(request, "home/homepage/home.html", context)


@cache_page(60 * 60 * 24 * 1)
@login_required
def top_word_posts(request):

    words = []

    if request.method == "GET":
        word = request.GET.get("w", None)
        posts_list = Post.objects.select_related("author").filter(
            author__public=True, content__unaccent__icontains=word
        )
        page = request.GET.get("page", 1)
        paginator = Paginator(posts_list, 10)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        """ get hot words and tags related to posts form tags """
        tags = cache.get("tt_post")
        top_words = cache.get("trending_words_posts")
        if top_words:
            words = top_words["phrases"]
            words = words + top_words["common_words"]

        context = {
            "posts": posts,
            "word": word,
            "is_word": True,
            "tags": tags,
            "words": words,
        }
        return render(request, "home/homepage/home.html", context)


@login_required
def post_create(request):

    data = dict()
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES or None)
        if form.is_valid():
            post = form.save(False)
            post.author = request.user
            post.save()
            if request.FILES is not None:
                images = [
                    request.FILES.get("images[%d]" % i)
                    for i in range(0, len(request.FILES))
                ]
                for i in images:
                    image_instance = Images.objects.create(image=i, post=post)
                    image_instance.save()
            data["form_is_valid"] = True
            data["post"] = render_to_string(
                "home/posts/new_post.html", {"post": post}, request=request
            )
            post.add_tags()
            try:
                async_send_mention_notifications.delay(post.author.id, post.id)
            except Exception as e:
                print(e.__class__)
                print(e)
        else:
            data["form_is_valid"] = False
    else:
        form = PostForm

    context = {
        "form": form,
    }
    data["html_form"] = render_to_string(
        "home/posts/post_create.html", context, request=request
    )
    return JsonResponse(data)


@login_required
def post_update(request, guid_url):
    data = dict()
    post = get_object_or_404(Post, guid_url=guid_url)
    if post.author == request.user:
        old_content = post.content
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            form.instance.author = request.user
            if form.is_valid():
                post = form.save()
                post.update_tags(old_content)
                post.update_mentions(old_content)
                data["form_is_valid"] = True
                data["post"] = render_to_string(
                    "home/posts/new_post.html", {"post": post}, request=request
                )
                try:
                    async_update_mention_notifications.delay(post.id, old_content)
                except Exception as e:
                    print(e.__class__)
                    print(e)
        else:
            form = PostForm(instance=post)
            form.instance.author = request.user
        data["html_form"] = render_to_string(
            "home/posts/post_update.html", {"form": form}, request=request
        )
        return JsonResponse(data)


@login_required
def post_delete(request, guid_url):
    data = dict()
    post = get_object_or_404(Post, guid_url=guid_url)
    if request.method == "POST":
        if post.author == request.user:
            try:
                async_delete_mention_notifications.delay(
                    post.author.id, post.id, post.content
                )
            except Exception as e:
                print(e.__class__)
                print(e)
            post.delete()
            data["form_is_valid"] = True
    else:
        context = {"post": post}
        data["html_form"] = render_to_string(
            "home/posts/post_delete.html", context, request=request
        )
    return JsonResponse(data)


@login_required
def post_detail(request, guid_url):

    data = dict()
    post = get_object_or_404(Post, guid_url=guid_url)
    context = {
        "post":post,
    }
    return render(request, "home/posts/post_detail.html", context)


@login_required
def post_comments(request, guid_url):
    
    data = dict()
    post = get_object_or_404(Post, guid_url=guid_url)
    comments_list = post.comments.select_related('name').filter(reply=None)
    page = request.GET.get("page", 1)
    paginator = Paginator(comments_list, 10)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)
    liked_by_viewer = set(Profile.objects.prefetch_related('comment_likes').get(id=request.user.id).comment_likes.values_list('id', flat=True))
    data['comments'] = json.loads(json.dumps(CommentSerializer(comments,context={'liked_by_viewer': liked_by_viewer}, many=True).data))
    data['has_next'] = comments.has_next() 
    data['page_number'] = page
    return JsonResponse(data, safe=False)
    
    
@login_required
def comment_replies(request, hid):
    
    data = dict()
    id = hashids.decode(hid)[0]
    comment = get_object_or_404(Comment, id=id)
    comment_list = comment.replies.select_related('name').order_by('created_on')
    page = request.GET.get("page", 1)
    paginator = Paginator(comment_list, 4)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)
    liked_by_viewer = set(Profile.objects.prefetch_related('comment_likes').get(id=request.user.id).comment_likes.values_list('id', flat=True))
    data['comments'] = json.loads(json.dumps(CommentSerializer(comments,context={'liked_by_viewer': liked_by_viewer}, many=True).data))
    data['has_next'] = comments.has_next() 
    data['parent_hashed_id'] = hid
    data['page_number'] = page
    return JsonResponse(data)

@login_required
def post_comment(request, guid_url):
    data = dict()
    post = get_object_or_404(Post, guid_url=guid_url)
    user = request.user
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(False)
            parent_comment = None
            parent_comment_id = request.POST.get("parent_comment_id", None)
            is_reply = request.POST.get("isReply", "false")
            print(is_reply)
            if parent_comment_id and is_reply == "true":
                id = hashids.decode(parent_comment_id)[0]
                parent_comment = get_object_or_404(Comment, id=id)
                # send reply notification
            comment.name = user
            comment.post = post
            comment.reply = parent_comment
            comment.save()
            c = comment.likes.count() 
            like_count = c if c > 0 else ''
            data['comment'] = json.loads(json.dumps(CommentSerializer(comment).data))
            data['post_comment_count'] = post.comments.filter(reply=None).count()
            # send comment notification 
        else:
            data['error'] = True
            data['error_message'] = "There was an issue posting your comment, please try again"
    return JsonResponse(data)

@login_required
def post_like(request, guid_url):
    data = dict()
    post = get_object_or_404(Post, guid_url=guid_url)
    user = request.user
    if request.method == "POST":
        if post.likes.filter(id=user.id).exists():
            post.likes.remove(user)
            try:
                message = "CON_POST" + " liked your post."
                actor_type = ContentType.objects.get_for_model(Profile)
                target_type = ContentType.objects.get_for_model(Post)
                post.author.notifications.filter(
                    actor_content_type__id=actor_type.id,
                    actor_object_id=request.user.id,
                    target_content_type__id=target_type.id,
                    target_object_id=post.id,
                    recipient=post.author,
                    verb=message,
                ).delete()
            except Exception as e:
                print(e.__class__)
                print("Error in removing like notification from post")

        else:
            post.likes.add(user)
            if user != post.author:
                if (
                    post.author.get_notify
                    and post.author.get_post_notify_all
                    and post.author.get_post_notify_likes
                ):
                    message = "CON_POST" + " liked your post."
                    notify.send(
                        sender=user, recipient=post.author, verb=message, target=post
                    )

        data["likescount"] = post.likes.count()
        return JsonResponse(data)

@login_required
def post_bookmark(request, guid_url):
    data = dict()
    post = get_object_or_404(Post, guid_url=guid_url)
    user = request.user
    return JsonResponse(data)

@login_required
def post_dropdown(request, guid_url):
    data = dict()
    post = get_object_or_404(Post, guid_url=guid_url)
    user = request.user
    if user.is_authenticated:
        if request.user == post.author:
            data['user_is_author'] = True
            data['post_edit_url'] = reverse("home:post-update", kwargs={"guid_url":post.guid_url})
            data['post_delete_url'] = reverse("home:post-delete", kwargs={"guid_url":post.guid_url})
        else:
            data['report_by_user_url'] = reverse("main:report-object", kwargs={"reporter_id":user.get_hashid()})
        data['post_hashid'] = post.get_hashid()
        data['has_bookmarked'] = True if BookmarkPost.objects.filter(user=user, obj_id=post.id).exists() else False
        return JsonResponse(data)
        
@login_required
def comment_options(request, hid):
    data = dict()
    id = hashids.decode(hid)[0]
    comment = get_object_or_404(Comment, id=id)
    if (request.user == comment.name) or (request.user == comment.post.author):
        data['viewer_can_delete'] = True
        data['comment_delete_url'] = reverse("home:comment-delete", kwargs={"hid":hid})
    else:
        data['viewer_can_delete'] = False
    if request.user != comment.name:
        data['viewer_can_report'] = True
        data['report_by_user_url'] = reverse("main:report-object", kwargs={"reporter_id":request.user.get_hashid()})
    else:
        data['viewer_can_report'] = True
    data['comment_hashed_id'] = hid
    return JsonResponse(data)

@login_required
def comment_like(request, hid):
    data = dict()
    id = hashids.decode(hid)[0]
    comment = get_object_or_404(Comment, id=id)
    user = request.user
    if request.method == "POST":
        if comment.likes.filter(id=user.id).exists():
            comment.likes.remove(user)
            data['is_liked'] = False
            try:
                message = (
                    "CON_POST"
                    + " liked your comment on "
                    + comment.post.author.get_full_name()
                    + "'s post."
                )
                description = comment.body
                actor_type = ContentType.objects.get_for_model(Profile)
                target_type = ContentType.objects.get_for_model(Post)
                action_type = ContentType.objects.get_for_model(Comment)
                # remove notification sent to comment author that user liked their notification
                comment.name.notifications.filter(
                    actor_content_type__id=actor_type.id,
                    actor_object_id=user.id,
                    target_content_type__id=target_type.id,
                    target_object_id=comment.post.id,
                    recipient=comment.name,
                    verb=message,
                    action_object_content_type__id=action_type.id,
                    action_object_object_id=comment.id,
                ).delete()
                # remove notification from post author's notification list
                message = "CON_POST" + " liked a comment on your post"
                comment.post.author.notifications.filter(
                    actor_content_type__id=actor_type.id,
                    actor_object_id=user.id,
                    target_content_type__id=target_type.id,
                    target_object_id=comment.post.id,
                    recipient=comment.post.author,
                    verb=message,
                    action_object_content_type__id=action_type.id,
                    action_object_object_id=comment.id,
                ).delete()
            except Exception as e:
                print(e.__class__)
                print("Error removing notification from liked comment")
        else:
            comment.likes.add(user)
            data['is_liked'] = True
            try:
                if user != comment.name:
                    if (
                        comment.name.get_notify
                        and comment.name.get_post_notify_all
                        and comment.name.get_post_notify_comments
                    ):
                        message = (
                            "CON_POST"
                            + " liked your comment on "
                            + comment.post.author.get_full_name()
                            + "'s post."
                        )
                        description = comment.body
                        notify.send(
                            sender=user,
                            recipient=comment.name,
                            verb=message,
                            description=description,
                            target=comment.post,
                            action_object=comment,
                        )
                if user != comment.post.author:
                    if (
                        comment.post.author.get_notify
                        and comment.post.author.get_post_notify_all
                        and comment.post.author.get_post_notify_comments
                    ):
                        message = "CON_POST" + " liked a comment on your post"
                        description = comment.body
                        notify.send(
                            sender=user,
                            recipient=comment.post.author,
                            verb=message,
                            description=description,
                            target=comment.post,
                            action_object=comment,
                        )
            except:
                print(
                    "error in sending notification to on post-comment-like --- "
                    + str(comment.name.id)
                    + str(comment.post.author)
                )
        c = comment.likes.count()
        data['like_count'] = c if c > 0 else ''
        return JsonResponse(data)


@login_required
def comment_delete(request, hid):
    data = dict()
    id = hashids.decode(hid)[0]
    comment = get_object_or_404(Comment, id=id)
    if request.method == "POST":
        if comment.name == request.user or request.user == comment.post.author:

            try:
                actor_type = ContentType.objects.get_for_model(Profile)
                target_type = ContentType.objects.get_for_model(Post)
                action_type = ContentType.objects.get_for_model(Comment)

                """
                Delete notification for comment, post author.
                Comment can either be a reply, or a parent comment, in both cases notification for comment's post's author should be deleted.
                """
                description = "Reply: " + comment.body
                message_comment = (
                    "CON_POST"
                    + " replied to your comment on "
                    + comment.post.author.get_full_name()
                    + "'s post."
                )  # message comment is sent to the parent comment
                message_post = (
                    "CON_POST" + " replied to a comment on your post."
                )  # message_post is sent to the post author of the reply's parent comment

                if comment.is_reply:
                    # the comment is a reply - delete te notification sent to the parent comment
                    comment.reply.name.notifications.filter(
                        actor_content_type__id=actor_type.id,
                        actor_object_id=comment.name.id,
                        target_content_type__id=target_type.id,
                        target_object_id=comment.post.id,
                        recipient=comment.reply.name,
                        description=description,
                        verb=message_comment,
                        action_object_content_type__id=action_type.id,
                        action_object_object_id=comment.id,
                    ).delete()

                    # first case, if the comment is a reply the description would be as above
                    comment.post.author.notifications.filter(
                        actor_content_type__id=actor_type.id,
                        actor_object_id=comment.name.id,
                        target_content_type__id=target_type.id,
                        target_object_id=comment.post.id,
                        recipient=comment.post.author,
                        description=description,
                        verb=message_post,
                        action_object_content_type__id=action_type.id,
                        action_object_object_id=comment.id,
                    ).delete()

                # second case the comment is a parent comment. The description for parent comment is different
                message = (
                    "CON_POST" + " commented on your post."
                )  # message to send to post author when user comments on their post
                description = "Comment: " + comment.body
                comment.post.author.notifications.filter(
                    actor_content_type__id=actor_type.id,
                    actor_object_id=comment.name.id,
                    target_content_type__id=target_type.id,
                    target_object_id=comment.post.id,
                    recipient=comment.name,
                    description=description,
                    verb=message,
                    action_object_content_type__id=action_type.id,
                    action_object_object_id=comment.id,
                ).delete()
            except Exception as e:
                print(e.__class__)
                print(
                    "There is an with removing notifications for deleting comment on post"
                )

            comment.delete()
            data["form_is_valid"] = True
            data['post_comment_count'] = comment.post.comments.filter(reply=None).count()
            data['comment_reply_count'] = comment.reply.replies.count()
    else:
        context = {"comment": comment}
        data["html_form"] = render_to_string(
            "home/posts/comment_delete.html", context, request=request
        )
    return JsonResponse(data)


""" Method for returning a list of all users who liked a post """


@login_required
def post_liked_by(request, guid_url):
    data = dict()
    post = get_object_or_404(Post, guid_url=guid_url)
    post_likes_list = post.likes.all().order_by('username')
    page = request.GET.get("page", 1)
    paginator = Paginator(post_likes_list, 10)
    try:
        post_likes = paginator.page(page)
    except PageNotAnInteger:
        post_likes = paginator.page(1)
    except EmptyPage:
        post_likes = paginator.page(paginator.num_pages)

    data["list"] = render_to_string(
        "home/posts/user_like_list.html",
        {"post_likes": post_likes, "post": post},
        request=request,
    )
    data["html"] = render_to_string(
        "home/posts/post_like_list.html",
        {"post_likes": post_likes, "post": post},
        request=request,
    )
    return JsonResponse(data)


""" Method for returning a list of all users who commented on a post """


@login_required
def post_comment_list(request, guid_url):

    data = dict()
    post = get_object_or_404(Post, guid_url=guid_url)

    page = request.GET.get("page", 1)
    post_comment_list = post.comments.all()

    paginator = Paginator(post_comment_list, 10)
    try:
        post_comments = paginator.page(page)
    except PageNotAnInteger:
        post_comments = paginator.page(1)
    except EmptyPage:
        post_comments = paginator.page(paginator.num_pages)

    data["list"] = render_to_string(
        "home/posts/user_comment_list.html",
        {"post_comments": post_comments, "post": post},
        request=request,
    )
    data["html"] = render_to_string(
        "home/posts/post_comment_list.html",
        {"post_comments": post_comments, "post": post},
        request=request,
    )
    return JsonResponse(data)


@login_required
def course_list(request):
    course_list = request.user.courses.order_by("course_university", "course_code")

    page = request.GET.get("page", 1)
    paginator = Paginator(course_list, 3)
    try:
        courses = paginator.page(page)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        courses = paginator.page(paginator.num_pages)
    context = {"courses": courses, "ucl": "active", "tt": ": Courses"}
    return render(request, "home/courses/course_list.html", context)


@login_required
def course_dashboard(request):

    school_courses = top_school_courses = courses = course_list = top_courses = []
    course_count = 0
    course_list = request.user.courses.order_by("course_university","course_code") # get user's courses6 alphabetically
    
    """ get a list of users that user has blocked and save it to request.session """
    try:
        if request.session.get("blockers") == None:
            blockers_list = Block.objects.blocked(request.user)
            request.session["blockers"] = [u.id for u in blockers_list]
    except Exception as e:
        print(e)
        request.session["blockers"] = []
    finally:
        pass
    
    page = request.GET.get("page", 1)
    if page == 1: # only get these object when page is first loaded
        try: 
            top_school_courses_id = Course.objects.get_or_set_top_school_courses(user=request.user)[:15] # need to be ran again when user adds/removes/edits a course
            if len(top_school_courses_id) < 8:
                top_school_courses = None
                school_courses = CourseObject.objects.get_school_courses(university=request.user.get_university_slug())[:15]
            else:
                top_school_courses_id = [i['id'] for i in top_school_courses_id]
                preserved = Case(
                    *[When(pk=pk, then=pos) for pos, pk in enumerate(top_school_courses_id)]
                )
                top_school_courses = Course.objects.filter(id__in=top_school_courses_id).order_by(preserved)      
        except Exception as e:
            print(e.__class__)
            print(e)

    paginator = Paginator(course_list, 10)
    try:
        courses = paginator.page(page)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        courses = paginator.page(paginator.num_pages)

    context = {
        "top_courses": top_courses,
        "top_school_courses": top_school_courses,
        "top_school": request.user.university,
        "courses": courses,
        "yc": "active",
        "tt": ": Dashboard",
        "school_courses": school_courses,
    }
    return render(request, "home/courses/course_dashboard.html", context)


@login_required
def courses_instructor(request, par1, par2):
    course_list = []
    university = instructor = num_courses = num_students = num_reviews = None
    page = request.GET.get("page", 1)
    try:
        if page == 1: # only retrieve this content if we are on page 1 (Page is loaded for the first time)
            try:
                instructor = Professors.objects.filter(
                    name_slug=par2, university_slug=par1
                ).first()
            except Exception as e:
                print(e)   
            course_list = (
                    Course.objects.filter(
                        course_instructor_slug=par2, course_university_slug=par1
                    )
                    .order_by(
                        "course_code", "course_instructor_slug", "course_university_slug"
                    )
                    .distinct(
                        "course_code", "course_instructor_slug", "course_university_slug"
                    )
                )
            course_object = course_list.first()
            num_students = (
                    Profile.objects.prefetch_related('courses').filter(
                        courses__course_university_slug__iexact=par1,
                        courses__course_instructor_slug__iexact=par2,
                    )
                    .distinct("id")
                    .count()
                )

            if instructor == None:
                instructor = (
                    course_object.course_instructor_fn.capitalize()
                    + " "
                    + course_object.course_instructor.capitalize()
                )
                university = course_object.course_university
                try:
                    Professors.objects.create(
                        first_name=course_object.course_instructor_fn.strip().lower(),
                        last_name=course_object.course_instructor.strip().lower(),
                        university=university,
                    )
                except Exception as e:
                    print(e)
                num_courses = Course.objects.filter(
                    course_instructor_slug=par2, course_university_slug=par1
                ).distinct("course_code").count()
            else: 
                university = instructor.university
                num_courses = instructor.courses.count()
                num_reviews = instructor.get_reviews_count()
                instructor = (
                    instructor.first_name.capitalize()
                    + " "
                    + instructor.last_name.capitalize()
                )
            if num_courses:
                num_courses = (
                    str(num_courses) + " courses"
                    if num_courses > 1
                    else str(num_courses) + " course"
                )
                    
    except Exception as e:
        print(e)

    paginator = Paginator(course_list, 10)
    try:
        courses = paginator.page(page)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        courses = paginator.page(paginator.num_pages)
    
    context = {
        "courses": courses,
        "instructor": instructor,
        "university": university,
        "num_courses": num_courses,
        "num_students": num_students,
        "num_reviews": num_reviews
    }
    return render(request, "home/courses/instructor_course_list.html", context)


@login_required
def course_add(request):
    if request.method == "POST":
        form = CourseForm(request.POST or None)
        if form.is_valid():
            course = form.save(False)
            code = course.course_code.upper().replace(" ", "")
            uni = course.course_university.strip().lower()
            ins_fn = course.course_instructor_fn.strip().lower()
            ins = course.course_instructor.strip().lower()
            try:
                prof, crp = Professors.objects.get_or_create(
                    first_name__iexact=ins_fn,
                    last_name__iexact=ins,
                    university__iexact=course.course_university,
                )
                course_obj, crc = CourseObject.objects.get_or_create(
                    code__iexact=code, university__iexact=course.course_university
                )
                # add course_obj to prof course - via tasks
                add_course_to_prof.delay(
                    prof.id, course_obj.id
                )  
            except Exception as e:
                print(e.__class__)
                print("ERROR - adding course to prof object" + str(e))
            has_course = request.user.courses.filter(
                course_code=code,
                course_instructor_fn__iexact=ins_fn,
                course_instructor__iexact=ins,
                course_year=course.course_year,
                course_university__iexact=uni,
            ).exists()
            course_object = Course.objects.filter(
                course_code=code,
                course_instructor_fn__iexact=ins_fn,
                course_instructor__iexact=ins,
                course_year=course.course_year,
                course_university__iexact=uni,
                course_difficulty=course.course_difficulty,
            )
            if has_course:
                form = CourseForm
                storage = messages.get_messages(request)
                for _ in storage:
                    pass
                for _ in list(storage._loaded_messages):
                    del storage._loaded_messages[0]
                messages.error(request, "You have already added this course.")
                return redirect("home:courses-add")
            else:
                try:
                    add_user_to_course.delay( # add the student to enrolled students for that course - via tasks
                        request.user.id, course_obj.id
                    )
                    user_get_or_set_top_school_courses.delay(
                        request.user.id
                    )
                except Exception as e:
                    print(e.__class__)
                    print("ERROR - adding user to course -- UPDATE user courses -- " + str(e))
                if course_object.exists():
                    c = course_object.first()
                    request.user.courses.add(c)
                else:
                    course.save()
                    request.user.courses.add(course)
                adjust_course_avg_hash(course) # adjust the average for the course - after the user has added the course
                # clear previous messages before showing new mesage
                storage = messages.get_messages(request)
                for _ in storage:
                    pass
                for _ in list(storage._loaded_messages):
                    del storage._loaded_messages[0]
                messages.success(request, "{} with {} was successfully added to your courses.".format(course.course_code, course.get_instructor_fullname()))
                return redirect("home:courses-add")
    else:
        form = CourseForm()
        if len(request.user.university) > 1:
            form.fields["course_university"].initial = request.user.university
    context = {"form": form, "ac": "active", "tt": ": Add Course"}
    return render(request, "home/courses/course_add.html", context)

@login_required
def course_auto_add(
    request, course_code, course_instructor_slug, course_university_slug
):
    if course_instructor_slug == "ALL":
        course = Course.objects.filter(
            course_code=course_code,
            course_university_slug__iexact=course_university_slug,
        ).first()
    else:
        course = Course.objects.filter(
            course_instructor_slug__iexact=course_instructor_slug,
            course_code=course_code,
            course_university_slug__iexact=course_university_slug,
        ).first()

    course_obj = CourseObject.objects.get_or_create(
        code=course_code, university__iexact=course.course_university,
    )

    data = dict()
    if request.method == "POST":
        form = CourseForm(request.POST or none)
        if form.is_valid():
            course = form.save(False)
            course_exists = Course.objects.filter(
                course_code=course.course_code,
                course_instructor_fn__iexact=course.course_instructor_fn,
                course_instructor__iexact=course.course_instructor,
                course_year=course.course_year,
                course_university__iexact=course.course_university,
                course_difficulty=course.course_difficulty,
                course_prof_difficulty=course.course_prof_difficulty,
            ).exists()
            if course_exists:
                c = Course.objects.filter(
                    course_code=course.course_code,
                    course_instructor_fn__iexact=course.course_instructor_fn,
                    course_instructor__iexact=course.course_instructor,
                    course_year=course.course_year,
                    course_university__iexact=course.course_university,
                    course_difficulty=course.course_difficulty,
                    course_prof_difficulty=course.course_prof_difficulty,
                ).first()
                request.user.courses.add(c)
                data["message"] = "Course added successfully"
            else:
                course.save()
                request.user.courses.add(course)
                data["message"] = "Course added successfully"
            try:
                add_user_to_course.delay(request.user.id, course_object.id)
                adjust_course_avg_hash(course)
                user_get_or_set_top_school_courses.delay(
                        request.user.id
                    )
            except Exception as e:
                print(e)
            data["form_is_valid"] = True
    else:

        if course_instructor_slug == "ALL":
            form = CourseForm(
                initial={
                    "course_code": course.course_code,
                    "course_university": course.course_university,
                    "course_year": current_year(),
                }
            )
        else:
            form = CourseForm(
                initial={
                    "course_code": course.course_code,
                    "course_instructor_fn": course.course_instructor_fn,
                    "course_instructor": course.course_instructor,
                    "course_university": course.course_university,
                    "course_year": current_year(),
                }
            )

        form.fields["course_code"].widget.attrs["readonly"] = True
        form.fields["course_university"].widget.attrs["readonly"] = True
        form.fields["course_university"].widget.attrs["disabled"] = True

        context = {
            "form": form,
            "course": course,
        }
        data["html_form"] = render_to_string(
            "home/courses/course_auto_add.html", context, request=request
        )
    return JsonResponse(data)

@login_required
def course_add_form_get_obj(request):

    data = dict()
    course_code_list = instructor_list = []
    uni = request.GET.get("u", request.user.university)
    
    if uni == "University":
        if request.user.university != None:
            uni = request.user.university
        else:
            uni = None
    obj = request.GET.get(
        "o", None
    )  # value that is initially typed in in course or instructor field
    obj0 = request.GET.get(
        "oj", None
    )  # value that we want without previous data - one field is blank
    obj1 = request.GET.get(
        "ot", None
    )  # value that we want - if set to course we are looking for course
    is_fn = request.GET.get("is_fn", False)
    obj_text = request.GET.get("q", None)

    if obj != None and obj1 == "instructor":  # have the code and want the instructor
        instructor_list = Professors.objects.search(
            text=obj_text, university=uni, first_name=is_fn
        )[:12]

    if (
        obj != None and obj1 == "code"
    ):  # have the instructor and want the code, obj has to be set to value of course instructor field

        course_code_list = (
            Course.objects.values_list("course_code", flat=True)
            .annotate(
                trigram=TrigramSimilarity("course_code", obj_text),
                trigram_ins=TrigramSimilarity("course_instructor", obj),
            )
            .filter(
                course_university__unaccent__iexact=uni,
                trigram__gte=0.15,
                trigram_ins__gte=0.3,
            )
            .order_by("-trigram")
        )

        course_code_list = list( 
            dict.fromkeys(
                list(course_code_list)
                )
        )[:12] # remove duplicates from the initial list
        
        if len(course_code_list) < 11:
            course_code_list = (
                CourseObject.objects.values_list("code", flat=True)
                .annotate(trigram=TrigramSimilarity("code", obj_text))
                .filter(
                    (Q(university__unaccent__iexact=uni) & Q(trigram__gte=0.1))
                    | (Q(trigram__gte=0.5))
                )
                .order_by("-trigram", "code")[:12]
            )
    elif (
        obj0 == "instructor"
    ):  # if obj0 is instructor no value is provided and user wants list of of instructors

        instructor_list = Professors.objects.search(
            text=obj_text, university=uni, first_name=is_fn
        )[:12]

    elif obj0 == "code":  # if obj0 is code then user is requesting list of course codes
        course_code_list = (
            CourseObject.objects.values_list("code", flat=True)
            .annotate(trigram=TrigramSimilarity("code", obj_text))
            .filter(
                (Q(university__unaccent__iexact=uni) & Q(trigram__gte=0.1))
                | (Q(trigram__gte=0.5))
            )
            .order_by("-trigram", "code")[:12]
        )

    course_code_list = list(course_code_list)
    instructor_list = list(instructor_list)

    data = {"ins": instructor_list, "code": course_code_list}

    return JsonResponse(data)


@login_required
def course_edit(request, hid):
    try:
        id = hashids.decode(hid)[0]
    except Exception as e:
        print("ERROR - retrieving id for course edit -- " + e)
        id = -1
    course_init = get_object_or_404(Course, id=id)
    callback = request.GET.get("callback",None)
    if request.method == "POST":
        form = CourseEditForm(request.POST)
        if form.is_valid():
            course = form.save()
            uni = course.course_university.strip().lower()
            ins_fn = course.course_instructor_fn.strip().lower()
            ins = course.course_instructor.strip().lower()
            try:
                prof, crp = Professors.objects.get_or_create(
                    first_name__iexact=ins_fn,
                    last_name__iexact=ins,
                    university__iexact=course.course_university,
                )
                course_obj, crc = CourseObject.objects.get_or_create(
                    code__iexact=course.course_code, university__iexact=course.course_university
                )
                add_course_to_prof.delay(
                    prof.id, course_obj.id
                )  # add course_obj to prof course - via tasks
            except Exception as e:
                print(e.__class__)
                print("ERROR - UPDATE course prof error -- " + str(e))
            request.user.courses.remove(course_init)
            request.user.courses.add(course)
            try:
                adjust_course_avg_hash(course)
                adjust_course_avg_hash(course_init)
                user_get_or_set_top_school_courses.delay(request.user.id)
                remove_user_from_course.delay(request.user.id, course_init.id, course.id, course_obj.id)
            except Exception as e:
                print(e)
            return redirect("home:course-list") if callback == "dashboard" else redirect("home:course-dashboard")
    else:
        form = CourseEditForm(instance=course_init)
    context = {"form": form, "course": course_init}
    return render(request, "home/courses/course_edit.html", context)

@login_required
def course_remove(request, hid):
    data = dict()
    try:
        id = hashids.decode(hid)[0]
    except Exception as e:
        print("ERROR - retrieving id for course remove -- " + e)
        id = -1
    course = get_object_or_404(Course, id=id)
    if request.method == "POST":
        request.user.courses.remove(course)
        try:
            remove_user_from_course.delay(request.user.id, course.id, complete=True)
            adjust_course_avg_hash(course)
            user_get_or_set_top_school_courses.delay(request.user.id)
        except Exception as e:
            print(e)
        data["is_valid"] = True
        if request.user.courses.count() == 0:
            data["done"] = True
            return redirect("home:courses")
    else:
        context = {"course": course}
        data["html_form"] = render_to_string(
            "home/courses/course_remove.html", context, request=request
        )
    return JsonResponse(data)


@login_required
def course_vote(request, hid, code, status=None):
    data = dict()
    try:
        id = hashids.decode(hid)[0]
    except Exception as e:
        print("ERROR - retrieving id for course edit -- " + e)
        id = -1
    course = get_object_or_404(Course, id=id)
    code = code
    if request.method == "POST":
        if status == "like":
            if course.course_dislikes.filter(id=request.user.id).exists():
                course.course_dislikes.remove(request.user)
            course.course_likes.add(request.user)

        elif status == "dislike":
            if course.course_likes.filter(id=request.user.id).exists():
                course.course_likes.remove(request.user)
            course.course_dislikes.add(request.user)

        elif status == "rmv":
            if course.course_dislikes.filter(id=request.user.id).exists():
                course.course_dislikes.remove(request.user)
            if course.course_likes.filter(id=request.user.id).exists():
                course.course_likes.remove(request.user)

        data["course_vote"] = render_to_string(
            "home/courses/course_vote.html", {"course": course}, request=request
        )
        return JsonResponse(data)


@login_required
def course_detail(request, course_university_slug, course_instructor_slug, course_code):
    data = dict()
    cannot_review = False
    sortby = {
        "latest": "Latest",
        "cy": "Year",
    }
    page = request.GET.get("page", 1)
    sb = request.GET.get("sb", "latest")
    o = request.GET.get("rw", None)
    if o == "all" or course_instructor_slug == "ALL":
        link_get = True 
    else:
        link_get = False
    
    if course_instructor_slug == "ALL":
        course = (
                Course.objects.filter(
                    course_university_slug=course_university_slug,
                    course_code=course_code,
                )
                .first()
            )
    else:
        course = (
            Course.objects.filter(
                course_university_slug=course_university_slug,
                course_instructor_slug=course_instructor_slug,
                course_code=course_code,
            )
            .first()
        )
        
    taken = request.user.courses.filter(
        course_university_slug=course_university_slug,
        course_code=course_code,
        course_instructor_slug=course_instructor_slug,
    ).exists()
    try:
        cannot_review = (
            Review.objects.select_related("author","course")
            .filter(
                author=request.user,
                course__course_code=course_code,
                course__course_university_slug=course_university_slug,
                course__course_instructor_slug=course_instructor_slug,
            )
            .exists()
        )
    except Exception as e:
        print(e)
    reviews_count = course.reviews_count()
    reviews_all_count = course.reviews_all_count()
    if request.method == "POST":
        form = ReviewForm(request.POST or None)
        if form.is_valid():
            cr = (
                Review.objects.select_related("author","course")
                .filter(
                    author=request.user,
                    course__course_code=course_code,
                    course__course_university_slug=course_university_slug,
                    course__course_instructor_slug=course_instructor_slug,
                )
                .exists()
            )
            if not cr:
                review = form.save(False)
                review.author = request.user
                submit_button = request.POST.get("rw_submit")
                if submit_button == "anon":
                    review.is_anonymous = True
                review.course = course
                review.save()
                update_course_reviews_cache(course)
            else:
                pass
        data["reviews_count"] = course.reviews_count()
        data["reviews_all_count"] = course.reviews_all_count()
        data["review"] = render_to_string(
            "home/courses/new_review.html",
            {"review": review, "course": course},
            request=request,
        )
        return JsonResponse(data)
    else:
        form = ReviewForm()
        try:
            form.fields["body"].widget.attrs["placeholder"] = (
                "Write a review for "
                + course.course_code
                + " with "
                + course.course_instructor_fn.capitalize()
                + " "
                + course.course_instructor.capitalize()
            )
        except Exception as e:
            print(e.__class__)
    
    reviews_list = (
        course.get_reviews_all(order=sb) if o == "all" else course.get_reviews(order=sb)
    )

    try:
        if not link_get:
            paginator = Paginator(reviews_list, 15)
            try:
                reviews = paginator.page(page)
            except PageNotAnInteger:
                reviews = paginator.page(1)
            except EmptyPage:
                reviews = paginator.page(paginator.num_pages)
        else:
            reviews = reviews_list
    except Exception as e:
        reviews = None
        print(e)

    context = {
        "course": course,
        "reviews_count": reviews_count,
        "reviews_all_count": reviews_all_count,
        "reviews": reviews,
        "taken": taken,
        "form": form,
        "course_detail": True,
        "link_get": link_get,
        "sortby": sortby[sb],
        "cannot_review": cannot_review,
    }
    return render(request, "home/courses/course_detail.html", context)


@login_required
def get_course_instructor_list(request, code, university):

    data = dict()
    instructors = list(
        Course.objects.filter(
            course_code=code, course_university_slug__iexact=university
        )
        .values("id", "course_instructor_fn", "course_instructor", "course_instructor_slug", "course_university_slug")
        .order_by("course_instructor_fn", "course_instructor")
        .distinct("course_instructor_fn", "course_instructor")
    )
    for i in instructors:
        i["id"] = hashids.encode(i["id"])
    data["course_code"] = code
    data["course_university_slug"] = university
    data["instructors"] = instructors
    return JsonResponse(data)


@login_required
def user_course_reviews(request):

    try:
        course = course_code = course_instructor = course_reviews = ""
        course_university_slug = request.GET.get("course_university", None)
        course_instructor_slug = request.GET.get("course_instructor", None)
        course_code = request.GET.get("course_code", None)
        reviews = Review.objects.select_related("author","course").filter(
            author=request.user, course__course_code=course_code, course__course_university_slug=course_university_slug
        )
        course = Course.objects.filter(
            course_code=course_code,
            course_university_slug=course_university_slug,
            course_instructor_slug=course_instructor_slug,
        ).first()
        if course != None:
            course_instructor = (
                course.course_instructor_fn.capitalize()
                + " "
                + course.course_instructor.capitalize()
            )
            course_code = course.course_code
            context = {
                "reviews": reviews,
                "course": course,
                "course_instructor": course_instructor,
                "course_code": course_code,
            }
            return render(request, "home/courses/user_course_reviews.html", context)
        else:
            return render(
                request, "home/courses/user_course_reviews.html", {"is_error": True}
            )
    except Exception as e:
        print(e)
        return render(
            request, "home/courses/user_course_reviews.html", {"is_error": True}
        )


@login_required
def course_share(request, hid):
    data = dict()
    try:
        id = hashids.decode(hid)[0]
    except Exception as e:
        print("ERROR - retrieving id for course edit -- " + e)
        id = -1
    course = get_object_or_404(Course, id=id)
    if request.method == "POST":
        title = "Started taking a new course!"
        content = (
            "Hey! I am taking "
            + course.course_code
            + " with "
            + course.course_instructor_fn
            + " "
            + course.course_instructor_fn
            + "!"
        )
        author = request.user
        post = Post(title=title, content=content, author=author)
        post.save()

    data["html"] = render_to_string(
        "home/courses/course_shared.html", {"course": course}, request=request
    )
    return JsonResponse(data)


@login_required
def course_instructors(request, course_university_slug, course_code):
    average_complexity = complexities = None
    num_instructors = "No instructors found"
    course_list = (
        Course.objects.filter(
            course_university_slug=course_university_slug, course_code=course_code
        )
        .order_by("course_university_slug", "course_instructor_slug", "course_code")
        .distinct("course_university_slug", "course_instructor_slug", "course_code")
    )
    
    total_enrollments = CourseObject.objects.get(
                code=course_code, university_slug__iexact=course_university_slug,
        ).enrolled.count()
    if course_list:
        num_instructors = course_list.count()
        num_instructors = (
            str(num_instructors) + " Instructors"
            if num_instructors > 1
            else str(num_instructors) + " Instructor"
        )
        average_complexity, complexities = course_list.first().average_complexities()
    if len(course_list) > 0:
        uni = course_list.first().course_university
    else:
        uni = (
            Course.objects.filter(course_university_slug=course_university_slug)
            .first()
            .course_university
        )
    
    if uni == None:
        uni = request.user.university
        
    page = request.GET.get("page", 1)
    paginator = Paginator(course_list, 10)
    try:
        courses = paginator.page(page)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        courses = paginator.page(paginator.num_pages)

    context = {
        "code": course_code,
        "university": uni,
        "courses": courses,
        "num_instructors": num_instructors,
        "total_enrollments":total_enrollments,
        "average_complexity":average_complexity,
        "complexities":complexities
    }
    return render(request, "home/courses/course_instructors.html", context)


@login_required
def review_like(request, hid, hidc, status):

    data = dict()

    id1 = hashids.decode(hid)[0]
    id2 = hashids.decode(hidc)[0]

    review = get_object_or_404(Review, id=id1)
    course = get_object_or_404(Course, id=id2)

    user = request.user
    if request.method == "POST":
        if status == "like":

            """
            Send a notification to the review author that someone has disliked their review
                The identity of the user who performed the action (actor) will not be disclosed 
            """
            if review.author != user:
                message = (
                    "CON_CRRW" + "A student liked your review on "
                )  # in template course.code should be added in order to add link to page
                description = review.body
                notify.send(
                    sender=user,
                    recipient=review.author,
                    verb=message,
                    description=description,
                    target=course,
                    action_object=review,
                )

            review.dislikes.remove(user)
            review.likes.add(user)

        elif status == "dislike":
            review.likes.remove(user)
            review.dislikes.add(user)

            try:
                actor_type = ContentType.objects.get_for_model(Profile)
                target_type = ContentType.objects.get_for_model(Course)
                action_type = ContentType.objects.get_for_model(Review)
                message = (
                    "CON_CRRW" + "A student liked your review on "
                )  # in template course.code should be added in order to add link to page
                description = review.body
                review.author.notifications.filter(
                    actor_content_type__id=actor_type.id,
                    actor_object_id=user.id,
                    target_content_type__id=target_type.id,
                    target_object_id=course.id,
                    recipient=review.author,
                    description=description,
                    verb=message,
                    action_object_content_type__id=action_type.id,
                    action_object_object_id=review.id,
                ).delete()
            except Exception as e:
                print(e.__class__)
                print(
                    "There was an error removing notifications for course review like"
                )

        elif status == "rmvlike":
            review.likes.remove(user)

        elif status == "rmvdislike":
            review.dislikes.remove(user)

        elif status == "ulike":
            review.dislikes.remove(user)
            review.likes.add(user)
            if review.author != user:
                message = (
                    "CON_CRRW" + "A student liked your review on "
                )  # in template course.code should be added in order to add link to page
                description = review.body
                notify.send(
                    sender=user,
                    recipient=review.author,
                    verb=message,
                    description=description,
                    target=course,
                    action_object=review,
                )

        elif status == "udislike":
            review.likes.remove(user)
            review.dislikes.add(user)

    data["review"] = render_to_string(
        "home/courses/review_like.html",
        {"review": review, "course": course},
        request=request,
    )
    return JsonResponse(data)


@login_required
def review_delete(request, hidc, hid):

    data = dict()

    id1 = hashids.decode(hid)[0]
    id2 = hashids.decode(hidc)[0]

    review = get_object_or_404(Review, id=id1)
    course = get_object_or_404(Course, id=id2)

    if request.method == "POST":
        if review.author == request.user:
            review.delete()
            update_course_reviews_cache(course)
            cr = Review.objects.filter(
                author=request.user,
                course__course_code=course.course_code,
                course__course_university_slug=course.course_university_slug,
                course__course_instructor_slug=course.course_instructor_slug,
            ).exists()
            data["form_is_valid"] = True
            data["reviews_count"] = course.reviews_count()
            data["reviews_all_count"] = course.reviews_all_count()
            if not cr:
                data["can_review"] = True
                context = {"review": review, "course": course, "form": ReviewForm()}
                data["review_form"] = render_to_string(
                    "home/courses/course_review_form.html", context, request=request
                )
    else:
        context = {"review": review, "course": course}
        data["html_form"] = render_to_string(
            "home/courses/review_delete.html", context, request=request
        )
    return JsonResponse(data)


@login_required
def university_detail(request):

    blockers_id = request.session.get("blockers")
    user_list = []
    uni = request.GET.get("u", request.user.university)
    obj = request.GET.get("obj", "std")
    u_empty = ""
    load_src = None
    user_has_program = user_has_courses = False
    if uni == None:
        uni = ""

    if len(uni) < 1:
        add_uni = True if len(request.user.university) < 1 else False
        return render(
            request,
            "home/courses/university_detail.html",
            {"is_empty": True, "add_uni": add_uni},
        )

    uni = get_similar_university(uni)
    
    if len(uni) < 1:
        add_uni = True if len(request.user.university) < 1 else False
        return render(
            request,
            "home/courses/university_detail.html",
            {"is_empty": True, "add_uni": add_uni},
        )
        
    data = get_uni_info(uni)
    logo_path = None

    try:
        logo_path = static(
            "default/university/" + uni.lower().replace(" ", "") + ".png"
        )
        try:
            from register.settings.common import BASE_DIR as bsdir
            if finders.find(bsdir+"/"+logo_path) == None:
                logo_path = None
        except Exception as e:
            print(e)
    except Exception as e:
        logo_path = None

    try:
        if uni.strip().lower() == "incoming student":
            add_uni = True
            uni_list = UNI_LIST
            universities_list = cache.get("university_list_incoming_student_")
            if universities_list == None:
                universities_list = {}
                for uni in uni_list:
                    universities_list[uni] = {}
                    universities_list[uni]["user_count"] = Profile.objects.filter(
                        university__iexact=uni
                    ).count()
                    universities_list[uni]["course_count"] = (
                        Course.objects.filter(course_university__iexact=uni)
                        .distinct(
                            "course_code", "course_instructor", "course_instructor_fn"
                        )
                        .count()
                    )
                    universities_list[uni]["data"] = get_uni_info(uni)
                cache.set("university_list_incoming_student_", universities_list, 14400)

            page = request.GET.get("page", 1)
            paginator = Paginator(tuple(universities_list.items()), 12)
            try:
                universities = paginator.page(page)
            except PageNotAnInteger:
                universities = paginator.page(1)
            except EmptyPage:
                universities = paginator.page(paginator.num_pages)
            return render(
                request,
                "home/courses/university_detail_incoming_student.html",
                {"universities": universities, "add_uni": add_uni},
            )

    except Exception as e:
        print(e.__class__)
        print(e)

    if data == None:
        data = []

    user_list = (
        Profile.objects.filter(university__iexact=uni)
        .exclude(id__in=blockers_id)
        .order_by("username")
        .distinct("username")
    )
    cr = (
        CourseObject.objects.filter(university__iexact=uni)
        .annotate(enrollments=Count("enrolled"))
        .order_by("-enrollments","code",)
    )
    ins = (
        Professors.objects.filter(university__iexact=uni)
        .annotate(course_count=Count("courses"))
        .order_by("course_count","last_name", "first_name")
    )
    num_instructors = num_courses = num_enrolled = 0
    try:
        ins_count, cr_count = ins.count(), cr.count()
        if cr_count > 1:
            num_courses = "{val:,} courses at this university".format(val=cr_count)
        else:
            num_courses = "{val:,} course at this university".format(val=cr_count)
        if len(user_list) > 1:
            num_enrolled = "{val:,} students go here".format(val=len(user_list))
        else:
            if (len(user_list)) == 0:
                num_enrolled = "No student is enrolled here"
            else:
                num_enrolled = "{val:,} student goes here".format(val=len(user_list))
        if ins_count > 1:
            num_instructors = "{val:,} instructors teach here".format(val=ins_count)
        else:
            num_instructors = "{val:,} instructor teaches here".format(val=ins_count)
        
    except Exception as e:
        print(e)
        num_courses = (
            str(cr.count()) + " courses at this university"
            if cr.count() > 1
            else str(cr.count()) + " course at this university"
        )
        num_enrolled = (
            str(len(user_list)) + " students go here"
            if len(user_list) > 1
            else str(len(user_list)) + " goes here"
        )

    if obj == "std":
        if len(user_list) < 1:
            u_empty = "No student found"

        page = request.GET.get("page", 1)
        paginator = Paginator(user_list, 12)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)

        context = {
            "uni": uni,
            "logo_path": logo_path,
            "users": users,
            "sa": "-active",
            "u_empty": u_empty,
            "data": data,
            "num_enrolled": num_enrolled,
            "num_courses": num_courses,
            "num_instructors":num_instructors
        }
        return render(request, "home/courses/university_detail_students.html", context)

    elif obj == "crs":
        course_list = (
            cr.filter(enrollments__gte=1)
        )
        if course_list.count() < 1:
            u_empty = "No courses found"

        page = request.GET.get("page", 1)
        paginator = Paginator(course_list, 8)
        try:
            courses = paginator.page(page)
        except PageNotAnInteger:
            courses = paginator.page(1)
        except EmptyPage:
            courses = paginator.page(paginator.num_pages)

        context = {
            "uni": uni,
            "logo_path": logo_path,
            "courses": courses,
            "ca": "-active",
            "u_empty": u_empty,
            "data": data,
            "num_enrolled": num_enrolled,
            "num_courses": num_courses,
            "num_instructors":num_instructors
        }
        return render(request, "home/courses/university_detail_courses.html", context)

    elif obj == "ins":
        try:
            instructor_list = (
                ins.filter(course_count__gte=1)
            )

            if instructor_list.count() < 1:
                u_empty = "No instructors found"
        except Exception as e:
            print(e)
            print(e.__class__)
            instructor_list = []

        page = request.GET.get("page", 1)
        paginator = Paginator(instructor_list, 8)
        try:
            instructors = paginator.page(page)
        except PageNotAnInteger:
            instructors = paginator.page(1)
        except EmptyPage:
            instructors = paginator.page(paginator.num_pages)

        context = {
            "uni": uni,
            "logo_path": logo_path,
            "instructors": instructors,
            "ia": "-active",
            "u_empty": u_empty,
            "data": data,
            "num_enrolled": num_enrolled,
            "num_courses": num_courses,
            "num_instructors":num_instructors
        }
        return render(
            request, "home/courses/university_detail_instructors.html", context
        )

    else:
        return render(
            request, "home/courses/university_detail.html", {"is_empty": True}
        )


""" Method to show users that user may interact with based specifically on users courses and university + instructors
    Method to be executed and result to cached - receive query set from cache - method constructed on daily basis """

@login_required
def find_students(request):

    crs_active = prgm_active = ""
    student_list = students = None
    needs_uni_edit = needs_puni_edit = False

    sl = request.GET.get("sl", "prgm")

    if sl == "crs":
        course_codes = (
            request.user.courses.order_by(
                "course_code",
                "course_university",
                "course_instructor",
                "course_instructor_fn",
                "course_year",
            )
            .distinct(
                "course_code",
                "course_university",
                "course_instructor",
                "course_instructor_fn",
                "course_year",
            )
            .values_list("course_code")
        )
        crs_active = "-active"
        if request.user.university != "":
            student_list = Course.objects.same_courses(
                user=request.user,
                course_list=course_codes,
                university=request.user.university,
            )
        else:
            needs_uni_edit = True
    elif sl == "prgm":
        if request.user.university != "" and request.user.program != "":
            student_list = Profile.objects.same_program(
                user=request.user,
                program=request.user.program,
                university=request.user.university,
            )
        else:
            needs_puni_edit = True
        prgm_active = "-active"

    if student_list:
        page = request.GET.get("page", 1)
        paginator = Paginator(student_list, 10)
        try:
            students = paginator.page(page)
        except PageNotAnInteger:
            students = paginator.page(1)
        except EmptyPage:
            students = paginator.page(paginator.num_pages)

    context = {
        "students": students,
        "sl": sl,
        "prgm_active": prgm_active,
        "crs_active": crs_active,
        "needs_uni_edit": needs_uni_edit,
        "needs_puni_edit": needs_puni_edit,
        "fs": "active",
        "tt": ": Find Students",
    }

    return render(request, "home/courses/related_students/student_list.html", context)


@login_required
def get_course_mutual_students(request):

    hid = request.GET.get("id", None)
    obj = request.GET.get("o", "all")
    try:
        id = hashids.decode(hid)[0]
    except Exception as e:
        print("ERROR - retrieving id for course edit -- " + e)
        id = -1
    course = get_object_or_404(Course, id=id)

    if obj == "ins":
        student_list = Profile.objects.get_students(
            user=request.user,
            code=course.course_code,
            instructor=course.course_instructor,
            instructor_fn=course.course_instructor_fn,
            university=course.course_university,
        )
    elif obj == "all":
        student_list = (
            Profile.objects.filter(
                courses__course_code=course.course_code,
                courses__course_university=course.course_university,
            )
            .order_by("last_name", "first_name", "university")
            .distinct("last_name", "first_name", "university")
        )

    page = request.GET.get("page", 1)
    paginator = Paginator(student_list, 10)
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        students = paginator.page(1)
    except EmptyPage:
        students = paginator.page(paginator.num_pages)

    context = {"students": students, "course": course, "o": obj}

    return render(request, "home/courses/student_list.html", context)


@login_required
def course_list_manager(request):
    
    lists = request.user.course_lists.order_by("-created_on")
    context = {"lists": lists, "ml": "active", "tt": ": My Lists"}
    return render(request, "home/courses/course_lists/main_menu.html", context)

@login_required
def course_list_create(request):

    data = dict()

    if request.method == "POST":

        form = CourseListForm(request.POST)
        if form.is_valid():
            li = form.save(False)
            li.creator = request.user
            li.save()
            data["form_is_valid"] = True
            data["list"] = render_to_string(
                "home/courses/course_lists/list_obj.html", {"list": li}, request=request
            )
        else:
            data["form_is_valid"] = False
    else:
        form = CourseListForm
    context = {
        "form": form,
    }

    data["html_form"] = render_to_string(
        "home/courses/course_lists/list_create_form.html", context, request=request
    )
    return JsonResponse(data)


@login_required
def course_list_edit(request, hid):

    data = dict()
    fc = ""

    id = hashid_list.decode(hid)[0]
    li = get_object_or_404(CourseList, id=id)

    if request.method == "POST":
        form = CourseListForm(request.POST, instance=li)
        if form.is_valid():
            li = form.save(False)
            li.creator = request.user
            li.save()
            data["form_edit_is_valid"] = True
            data["new_url"] = reverse(
                "home:course-list-obj", kwargs={"hid": li.get_hashid()}
            )
            data["list"] = render_to_string(
                "home/courses/course_lists/list_obj.html", {"list": li}, request=request
            )
        else:
            data["form_is_valid"] = False
    else:
        form = CourseListForm(instance=li)
        form.instance.creator = request.user

    a = request.GET.get("a", None)
    if a == "re":
        fc = "form-redirect-go"

    context = {"form": form, "list": li, "fc": fc}

    data["html_form"] = render_to_string(
        "home/courses/course_lists/list_edit_form.html", context, request=request
    )
    return JsonResponse(data)


@login_required
def course_list_delete(request, hid):

    data = dict()
    id = hashid_list.decode(hid)[0]
    li = get_object_or_404(CourseList, id=id)

    if request.method == "POST":
        if li.creator == request.user:
            li.delete()
            data["form_delete_is_valid"] = True
            a = request.POST.get("ac", None)
            if a == "h":
                data["new_url"] = reverse("home:course-list-manager")
                data["redirect"] = True
    else:
        a = request.GET.get("a", None)
        context = {"list": li, "a": a}
        data["html_form"] = render_to_string(
            "home/courses/course_lists/list_delete_form.html", context, request=request
        )
    return JsonResponse(data)


@login_required
def course_list_obj(request, hid):

    id = hashid_list.decode(hid)[0]
    li = get_object_or_404(CourseList, id=id)

    num_items = li.added_courses.count()

    o = request.GET.get("ol", "co")
    if o:
        order = {
            "co": "-created_on",
            "cu": "course_university",
            "ci": "course_instructor",
            "cc": "course_code",
        }
        objects = li.added_courses.order_by(order[o])
    else:
        objects = li.added_courses.order_by("created_on")

    context = {
        "list": li,
        "courses": objects,
        "num_items": num_items,
        "ml": "active",
        o + "_selected": "selected",
    }
    return render(request, "home/courses/course_lists/course_list.html", context)


@login_required
def course_list_obj_add_course(request, hid):

    id = hashid_list.decode(hid)[0]
    li = get_object_or_404(CourseList, id=id)

    data = dict()

    if request.method == "POST":
        form = CourseListObjectsForm(request.POST)
        if form.is_valid():
            cr = form.save(False)
            cr.parent_list = li
            cr.author = request.user
            cr.save()
            data["form_crsaction_is_valid"] = True
            data["new_url"] = reverse(
                "home:course-list-obj", kwargs={"hid": li.get_hashid()}
            )
        else:
            data["form_is_valid"] = False
    else:
        form = CourseListObjectsForm()
        if not request.user.university == None:
            form.fields["course_university"].initial = request.user.university

    action_url = reverse("home:course-list-addcrs", kwargs={"hid": li.get_hashid()})
    context = {
        "form": form,
        "list": li,
        "title_m": "Add Course",
        "actionbtn_m": "Add",
        "form_class": "crs-itm-",
        "action_url": action_url,
    }

    data["html_form"] = render_to_string(
        "home/courses/course_lists/list_create_form.html", context, request=request
    )
    return JsonResponse(data)


@login_required
def course_list_obj_remove_course(request, hid, hid_item):

    data = dict()

    id = hashid_list.decode(hid)[0]
    id2 = hashids.decode(hid_item)[0]
    li = get_object_or_404(CourseList, id=id)
    crs = get_object_or_404(CourseListObjects, id=id2)

    if request.method == "POST":
        if li.creator == request.user and crs.author == request.user:
            crs.delete()
            data["form_crsaction_is_valid"] = True
            data["new_url"] = reverse(
                "home:course-list-obj", kwargs={"hid": li.get_hashid()}
            )
    else:
        action_url = reverse(
            "home:course-list-deletecrs",
            kwargs={"hid": li.get_hashid(), "hid_item": crs.get_hashid()},
        )
        context = {
            "list": li,
            "crs": crs,
            "delete_text": "Are you sure you want to permanently remove this item from your list?",
            "form_class": "crs-itm-",
            "action_url": action_url,
        }
        data["html_form"] = render_to_string(
            "home/courses/course_lists/list_delete_form.html", context, request=request
        )
    return JsonResponse(data)


@login_required
def course_list_obj_edit_course(request, hid, hid_item):

    data = dict()

    id = hashid_list.decode(hid)[0]
    id2 = hashids.decode(hid_item)[0]
    li = get_object_or_404(CourseList, id=id)
    crs = get_object_or_404(CourseListObjects, id=id2)

    if request.method == "POST":
        form = CourseListObjectsForm(request.POST, instance=crs)
        if li.creator == request.user and crs.author == request.user:
            crs = form.save(False)
            crs.parent_list = li
            crs.author = request.user
            crs.save()
            data["form_crsaction_is_valid"] = True
            data["new_url"] = reverse(
                "home:course-list-obj", kwargs={"hid": li.get_hashid()}
            )
    else:
        form = CourseListObjectsForm(instance=crs)
        action_url = reverse(
            "home:course-list-editcrs",
            kwargs={"hid": li.get_hashid(), "hid_item": crs.get_hashid()},
        )
        context = {
            "form": form,
            "list": li,
            "crs": crs,
            "form_class": "crs-itm-",
            "action_url": action_url,
        }
        data["html_form"] = render_to_string(
            "home/courses/course_lists/list_edit_form.html", context, request=request
        )
    return JsonResponse(data)


@login_required
def course_save(request, id):

    data = dict()
    id = hashids.decode(id)[0]
    course = get_object_or_404(Course, id=id)
    if request.method == "POST":
        if request.user.saved_courses.filter(
            course_instructor=course.course_instructor,
            course_university=course.course_university,
            course_code=course.course_code,
        ).exists():
            data["message"] = "You have already saved this course"
        else:
            request.user.saved_courses.add(course)
            data["message"] = (
                course.course_code
                + " with professor "
                + course.course_instructor
                + " has been successfully added to your saved courses"
            )
        return JsonResponse(data)


@login_required
def remove_saved_course(request, hid):

    data = dict()
    id = hashids.decode(hid)[0]
    course = get_object_or_404(Course, id=id)
    if request.method == "POST":
        request.user.saved_courses.remove(course)
    else:
        context = {
            "course": course,
        }
        data["html_form"] = render_to_string(
            "home/courses/saved-course-remove.html", context, request=request
        )
    return JsonResponse(data)


@login_required
def saved_courses(request):
    course_list = request.user.saved_courses.all().order_by("course_university","course_code")
    page = request.GET.get("page", 1)
    paginator = Paginator(course_list, 10)
    try:
        courses = paginator.page(page)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        courses = paginator.page(paginator.num_pages)
        
    context = {
        "courses": courses, 
        "sc": "active", 
        "tt": ": Saved Courses"
        }
    return render(
        request,
        "home/courses/user_saved_courses.html",
        context,
    )

@login_required
def blog(request):

    blogs_list = Blog.objects.get_blogs(user=request.user)

    page = request.GET.get("page", 1)
    paginator = Paginator(blogs_list, 10)
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)
    context = {
        "blogs": blogs,
    }

    return render(request, "home/blog/blog.html", context)


def blog_create(request):

    if request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(False)
            blog.author = request.user
            blog.save()
            form.save_m2m()
            return redirect("home:blog-detail", hid=blog.guid_url, t=blog.slug)
    else:
        form = BlogForm
    context = {
        "form": form,
    }
    return render(request, "home/blog/blog_create.html", context)


def blog_detail(request, hid, t):

    blog = get_object_or_404(Blog, guid_url=hid, slug=t)
    replies_count = blog.blog_replies.count()
    context = {"blog": blog, "replies_count": replies_count}
    return render(request, "home/blog/blog_detail.html", context)


@login_required
def blog_update(request, hid, t):

    data = dict()
    blog = get_object_or_404(Blog, guid_url=hid, slug=t)
    if blog.author == request.user:
        if request.method == "POST":
            form = BlogForm(request.POST, instance=blog)
            form.instance.author = request.user
            if form.is_valid():
                form.save()
                return redirect("home:blog-detail", hid=blog.guid_url, t=blog.slug)
        else:
            form = BlogForm(instance=blog)
            form.instance.author = request.user
            is_edit = True
            context = {
                "form": form,
                "blog": blog,
                "is_edit": is_edit,
            }
        return render(request, "home/blog/blog_create.html", context)


@login_required
def blog_delete(request, hid, t):

    data = dict()
    blog = get_object_or_404(Blog, guid_url=hid, slug=t)
    if request.method == "POST":
        if blog.author == request.user:
            blog.delete()
            data["form_is_valid"] = True
    else:
        context = {"blog": blog}
        data["html_form"] = render_to_string(
            "home/blog/blog_delete.html", context, request=request
        )
    return JsonResponse(data)


@login_required
def blog_like(request, guid_url):

    data = dict()
    blog = get_object_or_404(Blog, guid_url=guid_url)
    user = request.user
    if request.method == "POST":
        if blog.likes.filter(id=user.id).exists():
            blog.likes.remove(user)
            try:
                actor_type = ContentType.objects.get_for_model(Profile)
                target_type = ContentType.objects.get_for_model(Blog)
                message = "CON_BLOG" + "liked your blog."
                blog.author.notifications.filter(
                    actor_content_type__id=actor_type.id,
                    actor_object_id=user.id,
                    target_content_type__id=target_type.id,
                    target_object_id=blog.id,
                    recipient=blog.author,
                    verb=message,
                ).delete()
            except Exception as e:
                print(e.__class__)
                print("There was an error removing notification for liked blog")
        else:
            blog.likes.add(user)
            if (
                blog.author.get_notify
                and blog.author.get_blog_notify_all
                and blog.author.get_blog_notify_likes
            ):
                message = "CON_BLOG" + "liked your blog."
                notify.send(
                    sender=user, recipient=blog.author, verb=message, target=blog
                )
        data["blog_likes"] = render_to_string(
            "home/blog/blog_like.html", {"blog": blog}, request=request
        )
        return JsonResponse(data)


@login_required
def blog_replies(request, guid_url, slug):

    data = dict()
    blog = get_object_or_404(Blog, guid_url=guid_url, slug=slug)
    replies_list = blog.blog_replies.order_by("-date_replied")

    page = request.GET.get("page", 1)
    paginator = Paginator(replies_list, 10)
    try:
        replies = paginator.page(page)
    except PageNotAnInteger:
        replies = paginator.page(1)
    except EmptyPage:
        replies = paginator.page(paginator.num_pages)

    replies_count = blog.blog_replies.count()
    user = request.user
    if request.method == "POST":
        form = BlogReplyForm(request.POST or None)
        if form.is_valid():
            reply = form.save(False)
            reply.author = request.user
            reply.blog = blog
            reply.save()
            if user != blog.author:
                if (
                    blog.author.get_notify
                    and blog.author.get_blog_notify_all
                    and blog.author.get_blog_notify_comments
                ):
                    message = "CON_BLOG" + "replied to your blog post."
                    description = reply.content
                    notify.send(
                        sender=user,
                        recipient=blog.author,
                        description=description,
                        verb=message,
                        target=blog,
                        action_object=reply,
                    )
            data["form_is_valid"] = True
            data["new_reply"] = render_to_string(
                "home/blog/blog_reply_new.html",
                {"reply": reply, "blog": blog},
                request=request,
            )
            data["reply_count"] = num_format(blog.blog_replies.count())
            return JsonResponse(data)
    else:
        form = BlogReplyForm
    context = {
        "blog": blog,
        "form": form,
        "replies": replies,
        "replies_count": replies_count,
    }

    return render(request, "home/blog/blog_replies.html", context)


@login_required
def blog_reply_like(request, hid):

    data = dict()
    id = hashids.decode(hid)[0]
    reply = get_object_or_404(BlogReply, id=id)
    user = request.user
    if request.method == "POST":
        if reply.reply_likes.filter(id=user.id).exists():
            reply.reply_likes.remove(user)
            try:
                actor_type = ContentType.objects.get_for_model(Profile)
                target_type = ContentType.objects.get_for_model(Blog)
                action_type = ContentType.objects.get_for_model(BlogReply)
                message = "CON_BLOG" + "liked your reply."
                description = reply.content
                blog.author.notifications.filter(
                    actor_content_type__id=actor_type.id,
                    actor_object_id=user.id,
                    target_content_type__id=target_type.id,
                    target_object_id=blog.id,
                    recipient=blog.author,
                    verb=message,
                    action_object_content_type__id=action_type.id,
                    action_object_object_id=reply.id,
                ).delete()
            except Exception as e:
                print(e.__class__)
                print("There was an error removing notification for liked blog")
        else:
            reply.reply_likes.add(user)
            if user != reply.author:
                if (
                    reply.author.get_notify
                    and reply.author.get_blog_notify_all
                    and reply.author.get_blog_notify_comments
                ):
                    message = "CON_BLOG" + "liked your reply."
                    description = reply.content
                    notify.send(
                        sender=user,
                        recipient=reply.author,
                        description=description,
                        verb=message,
                        target=blog,
                        action_object=reply,
                    )
        data["reply_likes"] = render_to_string(
            "home/blog/blog_reply_like.html", {"reply": reply}, request=request
        )
        return JsonResponse(data)


@login_required
def blog_reply_delete(request, hid, guid_url):

    data = dict()
    id = hashids.decode(hid)[0]
    reply = get_object_or_404(BlogReply, id=id)
    blog = get_object_or_404(Blog, guid_url=guid_url)

    if request.method == "POST":
        if request.user == blog.author or request.user == reply.author:
            try:
                actor_type = ContentType.objects.get_for_model(Profile)
                target_type = ContentType.objects.get_for_model(Blog)
                action_type = ContentType.objects.get_for_model(BlogReply)
                message = "CON_BLOG" + "replied to your blog post."
                description = reply.content
                blog.author.notifications.filter(
                    actor_content_type__id=actor_type.id,
                    actor_object_id=reply.author.id,
                    target_content_type__id=target_type.id,
                    target_object_id=blog.id,
                    recipient=blog.author,
                    verb=message,
                    action_object_content_type__id=action_type.id,
                    action_object_object_id=reply.id,
                ).delete()
            except Exception as e:
                print(e.__class__)
                print(
                    "There was an error in removing the notification for deleted blog reply"
                )
            reply.delete()
            data["form_is_valid"] = True
            data["reply_count"] = num_format(blog.blog_replies.count())
    else:
        context = {"blog": blog, "reply": reply}
        data["html_form"] = render_to_string(
            "home/blog/blog_reply_delete.html", context, request=request
        )
    return JsonResponse(data)


@login_required
def blog_reply_edit(request, hid, guid_url, slug):

    data = dict()
    id = hashids.decode(hid)[0]
    reply = get_object_or_404(BlogReply, id=id)
    blog = get_object_or_404(Blog, guid_url=guid_url, slug=slug)

    if request.method == "POST":
        if request.user == blog.author or request.user == reply.author:
            form = BlogReplyForm(request.POST, instance=reply)
            form.instance.author = request.user
            if form.is_valid():
                form.save()
                return redirect(
                    "home:blog-replies", guid_url=blog.guid_url, slug=blog.slug
                )
    else:
        form = BlogReplyForm(instance=reply)
        context = {"form": form, "blog": blog, "reply": reply}
    return render(request, "home/blog/blog_replies_edit.html", context)


@login_required
def tags_post(request, slug):

    tag = get_object_or_404(Tag, slug=slug)
    blockers_id = request.session.get("blockers")

    posts_list = (
        Post.objects.select_related("author")
        .exclude(author__id__in=blockers_id)
        .filter(tags=tag)
        .order_by("-last_edited")
    )
    related_tags = Post.tags.most_common(extra_filters={"post__in": posts_list})[:5]
    num_obj = posts_list.count()
    if num_obj > 1:
        s = "posts"
    else:
        s = "post"
    page = request.GET.get("page", 1)
    paginator = Paginator(posts_list, 10)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    is_tag = True
    context = {
        "tag": tag,
        "posts": posts,
        "is_tag": is_tag,
        "num_obj": num_obj,
        "s": s,
        "related_tags": related_tags,
    }
    return render(request, "home/homepage/home.html", context)


@login_required
def tags_blog(request, slug):

    tag = get_object_or_404(Tag, slug=slug)
    blockers_id = request.session.get("blockers")

    blog_list = (
        Blog.objects.select_related("author")
        .exclude(author__id__in=blockers_id)
        .filter(tags=tag)
        .order_by("-last_edited")
    )
    related_tags = Blog.tags.most_common(extra_filters={"blog__in": blog_list})[:5]
    num_obj = blog_list.count()
    if num_obj > 1:
        s = "blogs"
    else:
        s = "blog"
    page = request.GET.get("page", 1)
    paginator = Paginator(blog_list, 10)
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)
    is_tag = True
    context = {
        "tag": tag,
        "blogs": blogs,
        "is_tag": is_tag,
        "num_obj": num_obj,
        "s": s,
        "related_tags": related_tags,
    }
    return render(request, "home/blog/blog.html", context)


@login_required
def search_mobile(request):
    return render(request, "home/search/search_mobile.html")


@login_required
def search(request):
    if request.method == "GET":
        search_term = request.GET.get("q", None)
        if not SearchLog.objects.filter(search_text__iexact=search_term).exists():
            search_term = search_term.lower()
            sl = SearchLog.objects.create(search_text=search_term)
            request.user.recent_searches.add(sl)
        elif SearchLog.objects.filter(search_text__iexact=search_term).exists():
            sl = SearchLog.objects.filter(search_text__iexact=search_term).first()
            request.user.recent_searches.add(sl)

        o = request.GET.get("o", None)
        if o == "top":

            posts = Post.objects.search_topresult(search_term)
            blogs = Blog.objects.search_topresult(search_term)
            users = Profile.objects.search_topresult(search_term)
            courses = Course.objects.search(search_term)[:3]

            related_terms = SearchLog.objects.related_terms(search_term)
            no_related = True if related_terms.count() < 1 else False

            empty = (
                False
                if (
                    posts.exists()
                    or blogs.exists()
                    or users.exists()
                    or courses.exists()
                )
                else True
            )

            context = {
                "posts": posts,
                "blogs": blogs,
                "users": users,
                "empty": empty,
                "related_terms": related_terms,
                "courses": courses,
                "q": search_term,
                "top_active": "-active",
                "no_related": no_related,
            }

            return render(request, "home/search/search_top.html", context)

        if o == "post":
            post_list = Post.objects.search(search_term)
            tags = Post.tags.most_common(extra_filters={"post__in": post_list})[:5]
            page = request.GET.get("page", 1)
            paginator = Paginator(post_list, 10)
            try:
                posts = paginator.page(page)
            except PageNotAnInteger:
                posts = paginator.page(1)
            except EmptyPage:
                posts = paginator.page(paginator.num_pages)
            context = {
                "posts": posts,
                "tags": tags,
                "q": search_term,
                "post_active": "-active",
            }
            return render(request, "home/search/search_post.html", context)

        if o == "blog":
            blog_list = Blog.objects.search(search_term)
            page = request.GET.get("page", 1)
            paginator = Paginator(blog_list, 10)
            try:
                blogs = paginator.page(page)
            except PageNotAnInteger:
                blogs = paginator.page(1)
            except EmptyPage:
                blogs = paginator.page(paginator.num_pages)
            context = {"blogs": blogs, "q": search_term, "blog_active": "-active"}
            return render(request, "home/search/search_blog.html", context)

        if o == "users":
            if len(search_term.split()) > 1:
                users_list = Profile.objects.search_combine(search_term)
            else:
                users_list = Profile.objects.search(search_term)

            page = request.GET.get("page", 1)
            paginator = Paginator(users_list, 10)
            try:
                users = paginator.page(page)
            except PageNotAnInteger:
                users = paginator.page(1)
            except EmptyPage:
                users = paginator.page(paginator.num_pages)
            context = {"users": users, "q": search_term, "users_active": "-active"}
            return render(request, "home/search/search_user.html", context)

        if o == "course":

            course_list = Course.objects.search(search_term)

            page = request.GET.get("page", 1)
            paginator = Paginator(course_list, 7)
            try:
                courses = paginator.page(page)
            except PageNotAnInteger:
                courses = paginator.page(1)
            except EmptyPage:
                courses = paginator.page(paginator.num_pages)
            context = {"courses": courses, "q": search_term, "course_active": "-active"}
            return render(request, "home/search/search_course.html", context)


@login_required
def search_dropdown(request):

    if request.method == "GET":
        search_term = request.GET.get("q", None)
        user_recent_search = [
            str(i) for i in request.user.recent_searches.order_by("-time_stamp")[:3]
        ]
        most_similar = [
            str(i)
            for i in SearchLog.objects.filter(
                search_text__icontains=search_term
            ).order_by("-time_stamp")[:4]
        ]
        top_users = Profile.objects.search_topresult(search_text=search_term)[:5]
        most_similar = most_similar + [
            u.first_name + " " + u.last_name for u in top_users
        ]

        data = {
            "search_user": user_recent_search,
            "search_top": most_similar,
        }

        return JsonResponse(data, safe=False)


@login_required
def remove_search(request):

    data = dict()
    term = request.GET.get("t", None)
    if request.method == "POST":
        if term:
            term = term.lower()
            if request.user.is_authenticated:
                search_object = SearchLog.objects.get(search_text=term)
                request.user.recent_searches.remove(search_object)
                data["indv_search_remove"] = True
                return JsonResponse(data)
        else:
            request.user.recent_searches.clear()
            data["all_search_remove"] = True
            return JsonResponse(data)
