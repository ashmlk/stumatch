
from hashids import Hashids
from django.forms import modelformset_factory
from .models import (
    Post,
    Comment,
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


def send_comment_notification(user_id, post_id, comment_id):
    user = Profile.objects.get(id=user_id)
    post = Post.objects.get(id=post_id)
    comment = Comment.objects.get(id=comment_id)
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
            
def send_reply_notification(user_id, post_id, reply_id, parent_comment_id):
    user = Profile.objects.get(id=user_id)
    post = Post.objects.get(id=post_id)
    reply = Comment.objects.get(id=reply_id)
    comment_qs = Comment.objects.get(id=parent_comment_id)
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
            description=reply.body,
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
            sender=user,
            recipient=post.author,
            verb=message_post,
            description=reply.body,
            target=post,
            action_object=comment_qs,
        )
    
