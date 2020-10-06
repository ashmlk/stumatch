from django.contrib.postgres.search import SearchVector
from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from main.models import Profile
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from register.settings.production import sg

@receiver(post_save, sender=Profile)
def update_search_vector_profile(sender, instance, **kwargs):
    Profile.objects.filter(pk=instance.pk).update(sv=SearchVector('username','first_name','last_name','university','program'))

@receiver(post_save, sender=Profile)
def user_signed_up_views(sender, instace, **kwargs):
    if kwargs['created']:
        message = Mail(
            from_email='JoinCampus Team <no-reply@joincampus.ca>',
            to_emails=instance.email,
            subject='Welcome to JoinCampus',
            html_content = render_to_string('new_user_email.html', {'first_name': instance.first_name.capitalize()})
            )
        try:
            response = sg.send(message)
        except Exception as e:
            print(e)

@receiver(user_signed_up, dispatch_uid="allauth_user_registration_sign_up_not_views")
def user_signed_up_(request, user, **kwargs):
    message = Mail(
        from_email='JoinCampus Team <no-reply@joincampus.ca>',
        to_emails=user.email,
        subject='Welcome to JoinCampus',
        html_content = render_to_string('new_user_email.html', {'first_name': user.first_name.capitalize()})
        )
    try:
        response = sg.send(message)
    except Exception as e:
        print(e)
        

