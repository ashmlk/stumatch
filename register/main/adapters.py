from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.models import EmailAddress
from django.forms import ValidationError


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):

        if sociallogin.is_existing:
            return
        if "email" not in sociallogin.account.extra_data:
            return
        try:
            email = sociallogin.account.extra_data["email"].lower()
            email_address = EmailAddress.objects.get(email__iexact=email)
        except EmailAddress.DoesNotExist:
            return

        user = email_address.user

        if not user.is_active:
            user.is_active = True
            email_address.verified = True
            email_address.save()
            user.save()
            sociallogin.connect(request, user)
        elif user.is_active:
            if email_address.verified == True:
                sociallogin.connect(request, user)
            elif email_address.verified == False:
                return
