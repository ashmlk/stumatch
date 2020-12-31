import re
from notifications.signals import notify
from main.models import Profile
from home.models import Post
from django.contrib.contenttypes.models import ContentType


def extract(text):
    try:
        extract = re.findall("\B@(?<!@@)(\w{1,31})", text)
        usernames = list(dict.fromkeys([i[1] for i in extract]))
        return usernames
    except Exception as e:
        print(e.__class__)
        return []


def send_mention_notifications(sender_id, post_id):

    try:
        post = Post.objects.get(id=post_id)
        sender = Profile.objects.get(id=sender_id)
        usernames = extract(post.content)
        actor_type = ContentType.objects.get_for_model(Profile)
        target_type = ContentType.objects.get_for_model(Post)
        # send notifications:
        for username in usernames:
            try:
                if Profile.objects.filter(username=username).exists():
                    receiver = Profile.objects.get(username=username)
                    message = "CON_MENT mentioned you in a post"
                    if sender != receiver:
                        if not receiver.notifications.filter(
                            actor_content_type__id=actor_type.id,
                            actor_object_id=sender.id,
                            target_content_type__id=target_type.id,
                            target_object_id=post.id,
                            recipient=receiver,
                            verb=message,
                        ).exists():
                            if (
                                receiver.get_notify
                                and receiver.get_post_notify_all
                                and receiver.get_post_notify_mentions
                            ):
                                notify.send(
                                    sender=sender,
                                    recipient=receiver,
                                    description=post.title,
                                    verb=message,
                                    target=post,
                                )
            except Exception as e:
                print(e.__class__)
                print(e)
    except Exception as e:
        print(e.__class__)


def delete_mention_notifications(sender_id, post_id, content):

    try:
        sender = Profile.objects.get(id=sender_id)
        usernames = extract(content)
        actor_type = ContentType.objects.get_for_model(Profile)
        target_type = ContentType.objects.get_for_model(Post)
        for username in usernames:
            try:
                if Profile.objects.filter(username=username).exists():
                    receiver = Profile.objects.get(username=username)
                    message = "CON_MENT mentioned you in a post"
                    if sender != receiver:
                        receiver.notifications.filter(
                            actor_content_type__id=actor_type.id,
                            actor_object_id=sender.id,
                            target_content_type__id=target_type.id,
                            target_object_id=post_id,
                            recipient=receiver,
                            verb=message,
                        ).delete()
            except Exception as e:
                print(e.__class__)
                print(e)
    except Exception as e:
        print(e.__class__)
        print(e)
