from django.contrib.postgres.search import SearchVector
from django.db.models.signals import post_save
from django.dispatch import receiver
from main.models import Profile

@receiver(post_save, sender=Profile)
def update_search_vector_profile(sender, instance, **kwargs):
    Profile.objects.filter(pk=instance.pk).update(sv=SearchVector('username','first_name','last_name','university','program'))
    