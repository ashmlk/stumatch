import re
from notifications.signals import notify
from main.models import Profile
from home.models import Post, Comment
from django.contrib.contenttypes.models import ContentType


def extract(text):
    try:
        usernames = re.findall(r'(?:@)([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)', text)
        return list(set(usernames))
    except Exception as e:
        print(e.__class__)
        return []


def send_mention_notifications(sender_id, post_id, usernames=None):

    try:
        post = Post.objects.get(id=post_id)
        sender = Profile.objects.get(id=sender_id)
        usernames = extract(post.content) if usernames == None else usernames
        actor_type = ContentType.objects.get_for_model(Profile)
        target_type = ContentType.objects.get_for_model(Post)
        # send notifications:
        for username in usernames:
            username = username.lstrip("@")
            try:
                if Profile.objects.filter(username=username).exists():
                    receiver = Profile.objects.get(username=username)
                    message = "CON_MENT mentioned you in a post"
                    if sender != receiver:
                        # reassure not sending notification for being mentioned in a post twice
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
                                try:
                                    post.mentions.add(receiver)
                                except Exception as e:
                                    print(e)
                                    print("ERROR -- POST MENTIONS: Error adding user {} from post mentions with post id {}".format(str(receiver.id),str(post_id)))
                                finally:
                                    pass
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

def delete_mention_notifications(sender_id, post_id, content, usernames=None):

    try:
        post = Post.objects.get(id=post_id)
        sender = Profile.objects.get(id=sender_id)
        usernames = extract(content) if usernames == None else usernames
        actor_type = ContentType.objects.get_for_model(Profile)
        target_type = ContentType.objects.get_for_model(Post)
        for username in usernames:
            try:
                if Profile.objects.filter(username=username).exists():
                    receiver = Profile.objects.get(username=username)
                    try:
                        post.mentions.remove(receiver)
                    except Exception as e:
                        print(e)
                        print("ERROR -- POST MENTIONS: Error removing user {} from post mentions with post id {}".format(str(receiver.id),str(post_id)))
                    finally:
                        pass
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


def update_mention_notifications(post_id, old_content):
    
    post = Post.objects.get(id=post_id)
    prev_usernames = extract(old_content)
    cur_usernames = extract(post.content)
    diff = list(set(prev_usernames) ^ set(cur_usernames))
    old_usernames, new_usernames = [], []
    for x in diff:
        if x in prev_usernames:
            old_usernames.append(x) 
        else:
            new_usernames.append(x)
    delete_mention_notifications(post.author.id, post.id, post.content, old_usernames)
    send_mention_notifications(post.author.id, post.id, new_usernames)
    
    
def send_mention_notifications_comments(sender_id, post_id, comment_id):
    try:
        post = Post.objects.get(id=post_id)
        comment = Commet.object.get(id=comment_id)
        sender = Profile.objects.get(id=sender_id)
        usernames = extract(post.content) if usernames == None else usernames
        actor_type = ContentType.objects.get_for_model(Profile)
        target_type = ContentType.objects.get_for_model(Post)
        # send notifications:
        for username in usernames:
            username = username.lstrip("@")
            try:
                if Profile.objects.filter(username=username).exists():
                    receiver = Profile.objects.get(username=username)
                    message = "CON_MENT mentioned you in a comment"
                    if sender != receiver:
                        # avoid sending duplicate notifications even if sender has mentioned use multiple times
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
                                    description=comment.body,
                                    verb=message,
                                    target=post,
                                )
            except Exception as e:
                print(e.__class__)
                print(e)
    except Exception as e:
        print(e.__class__)
        
        
def delete_mention_notifications_comments(sender_id, post_id, comment_body):

    try:
        post = Post.objects.get(id=post_id)
        sender = Profile.objects.get(id=sender_id)
        usernames = extract(comment_body) if usernames == None else usernames
        actor_type = ContentType.objects.get_for_model(Profile)
        target_type = ContentType.objects.get_for_model(Post)
        for username in usernames:
            try:
                if Profile.objects.filter(username=username).exists():
                    receiver = Profile.objects.get(username=username)
                    message = "CON_MENT mentioned you in a comment"
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