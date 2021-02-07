
from hashids import Hashids
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
from .post_guid import uuid2slug, slug2uuid
from django.urls import reverse
import datetime
from datetime import timedelta
from django.db.models.functions import Now
from django.utils.timezone import make_aware
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.core.cache import cache
from notifications.signals import notify
import json
from django.contrib.admin.options import get_content_type_for_model
from django.contrib.contenttypes.models import ContentType


def send_comment_notification(user, post, comment):
    if comment.name != post.author:
        if (
            post.author.get_notify
            and post.author.get_post_notify_all
            and post.author.get_post_notify_comments
        ):
            message = (
                "CON_POST" + " commented on your post."
            )  # message to send to post author when user comments on their post
            description = "Comment: " + comment.body
            notify.send(
                sender=user,
                recipient=post.author,
                verb=message,
                description=description,
                target=post,
                action_object=comment,
            )
            
def send_reply_notification(user, post, reply, parent_comment):
    comment_qs = parent_comment
    if (
        comment_qs.name.get_notify
        and comment_qs.name.get_post_notify_all
        and comment_qs.name.get_post_notify_comments
    ):
        message_comment = (
            "CON_POST"
            + " replied to your comment on "
            + post.author.get_username()
            + "'s post."
        )  # message comment is sent to the parent comment
        notify.send(
            sender=user,
            recipient=comment_qs.name,
            verb=message_comment,
            description=description,
            target=post,
            action_object=comment_qs,
        )
        
    if (
        post.author.get_notify
        and post.author.get_post_notify_all
        and post.author.get_post_notify_comments
    ):
        message_post = (
            "CON_POST" + " replied to a comment on your post."
        )  # message_post is sent to the post author of the reply's parent comment
        notify.send(
            sender=request.user,
            recipient=post.author,
            verb=message_post,
            description=description,
            target=post,
            action_object=comment_qs,
        )
    
