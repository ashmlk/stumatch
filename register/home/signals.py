from django.contrib.postgres.search import SearchVector
from django.db.models.signals import post_save
from django.dispatch import receiver
from home.models import Post, Blog, Buzz, Course, Professors
from django.template.loader import render_to_string
#from .tasks import update_instructor_courses

@receiver(post_save, sender=Post)
def update_search_vector_post(sender, instance, **kwargs):
    search_vector  = search_vector = SearchVector('title') + SearchVector('content')
    Post.objects.filter(pk=instance.pk).update(sv=search_vector)
    
    
@receiver(post_save, sender=Blog)
def update_search_vector_blog(sender, instance, **kwargs):
    search_vector = SearchVector('title') + SearchVector('content')
    Blog.objects.filter(pk=instance.pk).update(sv=search_vector)
    
@receiver(post_save, sender=Course)
def update_search_vector_course(sender, instance, **kwargs):
    Course.objects.filter(pk=instance.pk).update(sv=\
        SearchVector('course_code','course_instructor','course_instructor_fn','course_university','course_university_slug','course_instructor_slug'))

 
@receiver(post_save, sender=Course)
def add_course_to_instructor(sender, instance, **kwargs):
    try:
        update_instructor_courses.delay(instance)
    except Exception as e:
        print(e)
        print(e.__class__)

@receiver(post_save, sender=Professors)
def update_search_vector_professors(sender, instance, **kwargs): 
    search_vector = SearchVector('first_name') + SearchVector('last_name')
    Professors.objects.filter(pk=instance.pk).update(sv=search_vector)