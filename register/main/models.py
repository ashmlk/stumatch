from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

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

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Course(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="course", null=True) # <--- added
    course_code = models.CharField(max_length=20)
    course_instructor = models.CharField(max_length=200)
    date_taken = models.DateField('Academic year')

    def __str__(self):
	    return self.course_code


class Item(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)

    def __str__(self):
	    return self.text


