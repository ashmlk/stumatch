from django.db import models
from django.utils import timezone
from main.models import Profile
from django.urls import reverse
from django.core.validators import MaxLengthValidator

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