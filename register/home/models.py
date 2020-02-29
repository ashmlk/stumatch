from django.db import models
from django.utils import timezone
from main.models import Profile
from django.urls import reverse
from django.core.validators import MaxLengthValidator, MinValueValidator


def current_year():
    return datetime.date.today().year

def max_value_current_year(value):
    return MaxValueValidator(current_year())(value) 
 
# Create your models here.
class Post(models.Model):
    subject = models.CharField(max_length=100)
    content = models.TextField(validators=[MaxLengthValidator(250)])
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    last_edited= models.DateTimeField(auto_now=True)
    likes= models.ManyToManyField(Profile, blank=True, related_name='post_likes')
    
    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    
    def get_like_url(self):
        return reverse("posts:like-toggle", kwargs={"slug": self.slug})

    def get_api_like_url(self):
        return reverse("posts:like-api-toggle", kwargs={"slug": self.slug})

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.ForeignKey(Profile, on_delete=models.CASCADE)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)

class Course(models.Model):
    course = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='course')
    course_code = models.CharField(max_length=12)
    course_university = models.CharField(max_length=50)
    course_instructor = models.CharField(max_length=50)
    course_year = models.IntegerField(('year'), validators=[MinValueValidator(1984), max_value_current_year])
    course_semester = models.CharField(max_length=6)
    
    def __str__(self):
        return self.course_code




    