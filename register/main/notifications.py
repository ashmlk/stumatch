from .models import Profile
from django.contrib.contenttypes.models import ContentType
from friendship.models import Friend, Follow, Block, FriendshipRequest
from notifications.signals import notify

# delete canceled friendship notification model when user cancel friend request
def notification_canceled_friend_request(user_id, other_user_id):
    user = Profile.objects.get(id=user_id)
    other_user = Profile.objects.get(id=other_user_id)
    if FriendshipRequest.objects.filter(
        from_user=other_user, to_user=user
    ).exists():
        fr = FriendshipRequest.objects.get(from_user=other_user, to_user=user)
        try:
            message = "CON_FRRE" + "has sent you a friend request"
            user.notifications.filter(
                actor_content_type__id=actor_type.id,
                actor_object_id=other_user.id,
                target_content_type__id=target_type.id,
                target_object_id=fr.id,
                recipient=user,
                verb=message,
            ).delete()
        except Exception as e:
            print(e.__class__)
            print("There was an issue with deleting a friend request")

# delete notification when user accepts friend request
def notification_accepted_friend_request(user_id, other_user_id):
    user = Profile.objects.get(id=user_id)
    other_user = Profile.objects.get(id=other_user_id)
    actor_type = ContentType.objects.get_for_model(Profile)
    target_type = ContentType.objects.get_for_model(FriendshipRequest)
    fr = FriendshipRequest.objects.get(from_user=other_user, to_user=user)
    try:
        message = "CON_FRRE" + "has sent you a friend request"
        user.notifications.filter(
            actor_content_type__id=actor_type.id,
            actor_object_id=other_user.id,
            target_content_type__id=target_type.id,
            target_object_id=fr.id,
            recipient=user,
            verb=message,
        ).delete()
    except Exception as e:
        print(e.__class__)
        print("There was an issue with deleting a friend request")
    if other_user.get_friendrequestaccepted_notify:
            message = "CON_FRRE" + "has accepted your friend request"
            notify.send(sender=user, recipient=other_user, verb=message, target=fr)
    
# delete notification if user canceled friend request
def delete_notification_cancel_pending(user_id, other_user):
    user = Profile.objects.get(id=user_id)
    other_user = Profile.objects.get(id=other_user_id)
    actor_type = ContentType.objects.get_for_model(Profile)
    target_type = ContentType.objects.get_for_model(FriendshipRequest)
    fr = FriendshipRequest.objects.get(from_user=user, to_user=other_user)
    try:
        message = "CON_FRRE" + "has sent you a friend request"
        other_user.notifications.filter(
            actor_content_type__id=actor_type.id,
            actor_object_id=user.id,
            target_content_type__id=target_type.id,
            target_object_id=fr.id,
            recipient=other_user,
            verb=message,
        ).delete()
    except Exception as e:
        print(e.__class__)
        print("There was an issue with deleting a friend request")

# send notification when adding user:
def send_notification_add_user(user_id, other_user_id):
    user = Profile.objects.get(id=user_id)
    other_user = Profile.objects.get(id=other_user_id)
    if other_user.get_friendrequest_notify:
        fr = FriendshipRequest.objects.get(
            from_user=user, to_user=other_user
        )
        message = "CON_FRRE" + "has sent you a friend request"
        notify.send(
            sender=user, recipient=other_user, verb=message, target=fr
        )
