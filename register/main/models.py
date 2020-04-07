from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(AbstractUser):
    bio = models.TextField()
    university = models.CharField(max_length=50)
    image = models.ImageField(default='profile_image/profile_default.png', upload_to='profile_image', blank=True)
    friends = models.ManyToManyField("Profile", blank=True)
    
    def __str__(self):
        return self.username
    
    def get_absolute_url(self):
        return "{}".format(self.slug)
 

class FriendRequest(models.Model):
    to_user = models.ForeignKey("Profile", on_delete = models.CASCADE, related_name="to_user")
    from_user = models.ForeignKey("Profile",on_delete = models.CASCADE, related_name="from_user")
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "frorm {}, to {}".format(self.from_user.username, self.to_user.username)