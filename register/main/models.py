from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class RightsSupport(models.Model):
    class Meta:

        managed = False  # No database table creation or deletion  \
        # operations will be performed for this model.

        permissions = (

            ("add_user", "Can Create User"),
            ("view_user", "Can View Single User"),
            ("change_user", "Can Change User"),
            ("list_user", "Can View User List"),

            ("add_plan", "Can Create Plan"),
            ("view_plan", "Can View Single Plan"),
            ("change_plan", "Can Change Plan"),
            ("list_plan", "Can View Plan List"),
  )


class User(AbstractUser):
    CREATED = 0
    ACTIVE = 1
    BANNED = 2
    KICKED = 3
    UPGRADE = 4
    STS = (
        (CREATED, 'Just Created'),
        (ACTIVE, 'Activated'),
        (BANNED, 'Disabled'),
        (KICKED, 'Disabled'),
        (UPGRADE, 'Active'),
     )
    status = models.IntegerField(choices=STS, default=CREATED, blank=True, null=True)
    def __str__(self):
        return self.username 
    
 

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


