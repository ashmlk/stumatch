from django.contrib.postgres.search import SearchVector
from django.db.models.signals import post_save
from django.dispatch import receiver
from home.models import Post, Blog, Buzz, Course

@receiver(post_save, sender=Post)
def update_search_vector_post(sender, instance, **kwargs):
    Post.objects.filter(pk=instance.pk).update(sv=SearchVector('title','content'))
    
@receiver(post_save, sender=Buzz)
def update_search_vector_buzz(sender, instance, **kwargs):
    Buzz.objects.filter(pk=instance.pk).update(sv=SearchVector('title','content','nickname'))
    
@receiver(post_save, sender=Blog)
def update_search_vector_blog(sender, instance, **kwargs):
    Blog.objects.filter(pk=instance.pk).update(sv=SearchVector('title','content'))
    
@receiver(post_save, sender=Course)
def update_search_vector_course(sender, instance, **kwargs):
    Course.objects.filter(pk=instance.pk).update(sv=\
        SearchVector('course_code','course_instructor','course_university','course_university_slug','course_instructor_slug'))
