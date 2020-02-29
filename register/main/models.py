from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver



class Profile(AbstractUser):
    bio = models.TextField() 
    university = models.CharField(max_length=50)
    image = models.ImageField(upload_to='profile_image', blank=True)

    def __str__(self):
        return self.username
    

 

