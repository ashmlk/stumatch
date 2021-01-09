from django.contrib.postgres.search import SearchVector
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from allauth.account.signals import user_signed_up, email_confirmed, password_reset
from allauth.account.models import EmailAddress
from django.template.loader import render_to_string
from main.models import Profile
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from register.settings.production import sg
import random
from defender.utils import unblock_username, is_user_already_locked


@receiver(post_save, sender=Profile)
def update_search_vector_profile(sender, instance, **kwargs):
    Profile.objects.filter(pk=instance.pk).update(
        sv=SearchVector("username", "first_name", "last_name", "university", "program")
    )


@receiver(pre_save, sender=Profile, dispatch_uid="set_username_of_empty_profile")
def set_username(sender, instance, **kwargs):
    """
    Every time a use is saved, ensures that user has a certain username
    This method avoids users having username field set to null
    """
    if not instance.username:
        rand = random.getrandbits(64)
        username = "user" + str(rand)
        while Profile.objects.filter(username=username):
            rand = random.getrandbits(64)
            username = "user" + str(rand)
        instance.username = username
        

@receiver(pre_save, sender=Profile, dispatch_uid="check_username_of_profile")
def check_set_username(sender, instance, **kwargs):
    """
    Check everytime a use sets a new username
    to see if username already exists.
    Method ensures that no username will every be used twice, to avoid any integrity error.
    """
    if Profile.objects.filter(username=instance.username).count() > 1:
        rand = random.getrandbits(64)
        username = "user" + str(rand)
        while Profile.objects.filter(username=username):
            rand = random.getrandbits(64)
            username = "user" + str(rand)
        instance.username = username
        instance.save()


@receiver(post_save, sender=Profile, dispatch_uid="send_welcome_email_on_user_sign_up")
def user_signed_up_views(sender, instance, **kwargs):
    if kwargs["created"]:
        message = Mail(
            from_email="JoinCampus <no-reply@joincampus.ca>",
            to_emails=instance.email,
            subject="Welcome to JoinCampus",
            html_content=render_to_string(
                "new_user_email.html", {"first_name": instance.first_name.capitalize()}
            ),
        )
        try:
            response = sg.send(message)
        except Exception as e:
            print(e)


@receiver(user_signed_up, dispatch_uid="allauth_user_registration_sign_up_not_views")
def user_signed_up_(request, user, **kwargs):
    message = Mail(
        from_email="JoinCampus <no-reply@joincampus.ca>",
        to_emails=user.email,
        subject="Welcome to JoinCampus",
        html_content=render_to_string(
            "new_user_email.html", {"first_name": user.first_name.capitalize()}
        ),
    )
    try:
        response = sg.send(message)
    except Exception as e:
        print(e)


@receiver(email_confirmed)
def email_confirmed_(request, email_address, **kwargs):

    try:
        user = Profile.objects.get(email=email_address.email)
        user.is_active = True
        user.save()
    except Exception as e:
        print(e.__class__)


@receiver(password_reset, dispatch_uid="allauth_user_reset_password_success")
def user_password_reset(request, user, **kwargs):
    try:
        if is_user_already_locked(user.username):
            unblock_username(user.username)
    except Exception as e:
        print(e.__class__)
        print(e)
