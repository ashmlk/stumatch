from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_uuid_upload import upload_to_uuid
from taggit.models import Tag
from django.contrib.postgres.search import SearchVector
from django.contrib.postgres.search import SearchQuery
from django.contrib.postgres.search import SearchRank
from django.contrib.postgres.indexes import GinIndex
import django.contrib.postgres.search as pg_search
from django.db.models.functions import Greatest

#CUSTOM MODEL MANAGERS
class ProfileManager(models.Manager):
    
    def search(self, search_text):
        search_vectors = ( 
              SearchVector(
                  'username', weight='A', config='english'
            
                ) + SearchVector(
                  'first_name', 'last_name' , weight='B', config='english'
                ) + SearchVector(
                  'bio', weight='C', config='english'
            
                )
              )
        search_query = SearchQuery(
            search_text, config=' english__unaccent'
        )
        search_rank = SearchRank(search_vectors,search_query)
        trigram = TrigramSimilarity(
            'username',search_text
        ) + TrigramSimilarity(
            'last_name',search_text
        ) 
        qs = (
            self.get_queryset()
            .filter(sv=search_query)
            .annotate(rank=search_rank, trigram=trigram, bs=Greatest('rank','trigram'))
            .filter(Q(bs__gte=0.35))
            .order_by('-bs')
        )
        
        return qs

class Profile(AbstractUser):
    bio = models.TextField()
    university = models.CharField(max_length=50)
    program = models.CharField(blank=True,max_length=100)
    image = models.ImageField(default='defaults/user/default_u_i.png', upload_to=upload_to_uuid('profile_image/profiles/'), blank=True)
    courses = models.ManyToManyField('home.Course',related_name='profiles')
    saved_courses = models.ManyToManyField('home.Course',related_name='saved_courses')
    favorite_post_tags = models.ManyToManyField(Tag, related_name='fav_post_tags')
    favorite_buzz_tags = models.ManyToManyField(Tag, related_name='fav_buzz_tags')
    favorite_blog_tags = models.ManyToManyField(Tag, related_name='fav_blog_tags')
    sv = pg_search.SearchVectorField(null=True)
    
    objects = ProfileManager()
    
    class Meta:
        indexes = [
            GinIndex(fields=['sv'],name='search_idx_user'),
        ]
        
    def __str__(self):
        return self.username
    
    def get_absolute_url(self):
        return "{}".format(self.slug)


class BookmarkBase(models.Model):
    class Meta:
        abstract = True
        
    user = models.ForeignKey(Profile,on_delete=models.CASCADE, verbose_name="User")

    def __str__(self):
        return self.user.username

class BookmarkPost(BookmarkBase):
    class Meta:
        db_table  = "bookmark_post"
    
    date = models.DateTimeField(auto_now_add=True)
    obj = models.ForeignKey('home.Post',on_delete=models.CASCADE, verbose_name="Post")

class BookmarkBlog(BookmarkBase):
    class Meta:
        db_table  = "bookmark_blog"
        
    date = models.DateTimeField(auto_now_add=True)
    obj = models.ForeignKey('home.Blog',on_delete=models.CASCADE, verbose_name="Blog")

class BookmarkBuzz(BookmarkBase):
    class Meta:
        db_table  = "bookmark_buzz"
        
    date = models.DateTimeField(auto_now_add=True)
    obj = models.ForeignKey('home.Buzz',on_delete=models.CASCADE, verbose_name="Buzz")
    
