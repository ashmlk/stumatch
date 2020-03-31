from django.db import models
from django.utils import timezone
from main.models import Profile
from django.urls import reverse
from django.core.validators import MaxLengthValidator, MinValueValidator
import uuid


def current_year():
    return datetime.date.today().year

def max_value_current_year(value):
    return MaxValueValidator(current_year())(value) 
 
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(validators=[MaxLengthValidator(250)])
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)
    last_edited= models.DateTimeField(auto_now=True)
    likes= models.ManyToManyField(Profile, blank=True, related_name='post_likes')
    
    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse('home:home')
    
    def get_like_url(self):
        return reverse("home:like-toggle", kwargs={'pk': self.pk})

    def get_api_like_url(self):
        return reverse("home:like-api-toggle", kwargs={'pk': self.pk})

def image_create_uuid_p_u(instance, filename):
    return '/'.join(['post_images', str(instance.post.id), str(uuid.uuid4().hex + ".png")]) 

class Images(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    image = models.FileField(upload_to=image_create_uuid_p_u,verbose_name='Image')
    date_added = models.DateTimeField(auto_now_add=True)
    
class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.ForeignKey(Profile, on_delete=models.CASCADE)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)

class Course(models.Model):
    course = models.ManyToManyField(Profile,related_name='course')
    course_code = models.CharField(max_length=12)
    course_university = models.CharField(max_length=50)
    course_instructor = models.CharField(max_length=50)
    course_year = models.IntegerField(('year'), validators=[MinValueValidator(1984), max_value_current_year])
    course_semester = models.CharField(max_length=6)
    
    def __str__(self):
        return self.course_code




    