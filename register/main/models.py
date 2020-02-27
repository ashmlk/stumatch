from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver



class Profile(AbstractUser):
    # remove email fields
    bio = models.TextField() 
    university = models.CharField(max_length=30)

    def __str__(self):
        return self.username
    

 
'''
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=150)
    bio = models.TextField() 
    university = models.CharField(max_length=30)
    

    def __str__(self):
        return self.user.username
        
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=AbstractUser)

@receiver(post_save, sender=Profile)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

'''


