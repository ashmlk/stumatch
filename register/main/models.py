from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_uuid_upload import upload_to_uuid
from taggit.models import Tag
from django.contrib.postgres.search import (SearchQuery, SearchRank, SearchVector, TrigramSimilarity,)
from django.contrib.postgres.aggregates import StringAgg
from django.contrib.postgres.indexes import GinIndex
import django.contrib.postgres.search as pg_search
from django.db.models.functions import Greatest
from django.contrib.auth.models import BaseUserManager
from django.core.validators import MaxLengthValidator, MinValueValidator, MaxValueValidator
from django.db.models import Q, F, Count, Avg, FloatField
from hashids import Hashids
from friendship.models import Friend, Follow, Block, FriendshipRequest

hashids_user = Hashids(salt='wvf935 vnw9py l-itkwnhe 3094',min_length=12)

#CUSTOM MODEL MANAGERS
class ProfileManager(BaseUserManager):
    
    def same_program(self, user, program, university):
        
        usernames = [user.username]
        friends = Friend.objects.friends(user)
        blocked =  Block.objects.blocking(user)
        
        if friends:
            for f in friends:
                usernames.append(str(f))
        if blocked:
            for b in blocked:
                usernames.append(str(b))
            
        search_vectors = ( 
   
                    SearchVector(
                        StringAgg('university', delimiter=' '), 
                        weight='B', config='english'
                    
                    ) + SearchVector(
                        StringAgg('program', delimiter=' '), 
                         weight='B', config='english'
                    )
        )
        
        qs = (
            self.get_queryset()
            .exclude(username__in=usernames) 
            .annotate(
                similarity_university = TrigramSimilarity('university', university),
                similarity_program = TrigramSimilarity('program', program)
            ).filter(
                (Q(university__unaccent__icontains=university) & Q(program__unaccent__icontains=program)) |
                (Q(similarity_university__gte=0.01) & Q(similarity_program__gte=0.01)) |
                (Q(similarity_program__gte=0.4)) 
            ).order_by('-similarity_university','-similarity_program')
        )
    
        return qs
    
    def search_topresult(self, search_text):
        
        search_text=search_text.strip()
        
        if len(search_text.strip()) < 2:
            qs = (
                self.get_queryset()
                .annotate(
                    trigram = Greatest(
                        TrigramSimilarity('username', search_text),
                        TrigramSimilarity('first_name', search_text),
                        TrigramSimilarity('last_name', search_text))
                    ).filter(
                        Q(username__unaccent__trigram_similar=search_text) |
                        Q(last_name__unaccent__trigram_similar=search_text) |
                        Q(first_name__unaccent__trigram_similar=search_text) |
                        Q(username__unaccent__icontains=search_text), trigram__gte=0.2
                    ).order_by('-trigram')
                )
            if qs.count() < 1:
                return self.search(search_text)[:5]
            else:
                 return qs
        
        else:
            
            search_text=search_text.strip()
        
            search_vectors = ( 
                SearchVector(
                    'last_name', weight='B', config='english'
                    
                    ) + SearchVector(
                        'username', delimiter=' ',
                        weight='A', config='english'
                        
                    ) + SearchVector(
                        'first_name', delimiter=' ',
                        weight='C', config='english'
                        
                    ) 
                )
            
            search_query = SearchQuery(
                search_text, config='english'
            )
            
            search_rank = SearchRank(search_vectors,search_query)
            
            if len(search_text.split()) == 2:
                #possibly name+lastname, lastname+name, username+lastname
                search_text_1 ,search_text_2 = search_text.split(' ', 1)
                
                trigram = (TrigramSimilarity(
                        'username', search_text
                    ) + TrigramSimilarity(
                        'last_name', search_text
                    ) + TrigramSimilarity(
                        'first_name', search_text
                    ) + TrigramSimilarity(
                        'username', search_text_1
                    ) + TrigramSimilarity(
                        'last_name', search_text_1
                    ) + TrigramSimilarity(
                        'first_name', search_text_1
                    ) + TrigramSimilarity(
                        'username', search_text_2
                    ) + TrigramSimilarity(
                        'last_name', search_text_2
                    ) + TrigramSimilarity(
                        'first_name', search_text_2
                    ) 
                )
                
            else:
                
                trigram = (TrigramSimilarity(
                        'username', search_text
                    ) + TrigramSimilarity(
                        'last_name', search_text
                    ) + TrigramSimilarity(
                        'first_name', search_text
                    ) 
                )
                
            
            qs = (
                self.get_queryset()
                .annotate(rank=search_rank, trigram = trigram)
                .filter(
                    Q(rank__gte=0.3)|
                    Q(username__unaccent__trigram_similar=search_text) |
                    Q(last_name__unaccent__trigram_similar=search_text) |
                    Q(first_name__unaccent__trigram_similar=search_text), trigram__gte=0.1
                ).order_by('-rank')[:5]
            )
            
            if qs.count() < 1:
                return self.search_combine(search_text)[:5]
            else:
                 return qs


    def search(self, search_text):

        search_text=search_text.strip()
        
        qs = (
            self.get_queryset()
            .annotate(
                trigram = Greatest(
                    TrigramSimilarity('username', search_text),
                    TrigramSimilarity('first_name', search_text),
                    TrigramSimilarity('last_name', search_text))
                ).filter(
                    Q(username__unaccent__trigram_similar=search_text) |
                    Q(last_name__unaccent__trigram_similar=search_text) |
                    Q(first_name__unaccent__trigram_similar=search_text) |
                    Q(username__unaccent__icontains=search_text), trigram__gte=0.03
                ).order_by('-trigram')
            )
        return qs
        
        
    def search_combine(self, search_text):
        
        search_text=search_text.strip()
        
        search_vectors = ( 
              SearchVector(
                  'last_name', weight='B', config='english'
                  
                ) + SearchVector(
                    'username', delimiter=' ',
                    weight='A', config='english'
                    
                ) + SearchVector(
                    'first_name', delimiter=' ',
                    weight='C', config='english'
                    
                ) 
              )
        
        search_query = SearchQuery(
            search_text, config='english'
        )
        
        search_rank = SearchRank(search_vectors,search_query)
        
        if len(search_text.split()) == 2:
            #possibly name+lastname, lastname+name, username+lastname
            search_text_1 ,search_text_2 = search_text.split(' ', 1)
            
            trigram = (TrigramSimilarity(
                    'username', search_text
                ) + TrigramSimilarity(
                    'last_name', search_text
                ) + TrigramSimilarity(
                    'first_name', search_text
                ) + TrigramSimilarity(
                    'username', search_text_1
                ) + TrigramSimilarity(
                    'last_name', search_text_1
                ) + TrigramSimilarity(
                    'first_name', search_text_1
                ) + TrigramSimilarity(
                    'username', search_text_2
                ) + TrigramSimilarity(
                    'last_name', search_text_2
                ) + TrigramSimilarity(
                    'first_name', search_text_2
                ) 
            )
        
        else:
            
            trigram = (TrigramSimilarity(
                        'username', search_text
                    ) + TrigramSimilarity(
                        'last_name', search_text
                    ) + TrigramSimilarity(
                        'first_name', search_text
                    ) 
                )
            
            
        
        qs = (
            self.get_queryset()
            .annotate(rank=search_rank, trigram = trigram)
            .filter(
                Q(rank__gte=0.2)|
                Q(username__unaccent__trigram_similar=search_text) |
                Q(last_name__unaccent__trigram_similar=search_text) |
                Q(first_name__unaccent__trigram_similar=search_text), trigram__gte=0.03
            ).order_by('-rank')
        )
        
        return qs

class SearchLogManager(models.Manager):
    
    def related_terms(self, term):
        
        search_vectors = ( 
              SearchVector(
                  'search_text', weight='A', config='english'
                )
            )
        
        similarity = TrigramSimilarity('search_text', term)
        
        search_query = SearchQuery(
            term, config='english'
        )
        
        search_rank = SearchRank(search_vectors,search_query)
        
        qs = (
            self.get_queryset()
            .filter(~Q(search_text__iexact=term))
            .annotate(rank=search_rank, trigram = similarity)
            .filter(
                Q(rank__gte=0.2)|
                Q(trigram__gte=0.1)
            ).annotate(
                count=Count('recent_searches')
            ).order_by('-rank','count','-time_stamp')
        )
        
        return qs
    
class SearchLog(models.Model):
    
    time_stamp =  models.DateTimeField(auto_now_add=True)
    search_text = models.TextField(db_index=True)
    
    objects = SearchLogManager()
    
    def __str__(self):
        return self.search_text     
        
        
class Profile(AbstractUser):
    bio = models.TextField()
    university = models.CharField(max_length=50)
    program = models.CharField(blank=True,max_length=100)
    image = models.ImageField(default='defaults/user/default_u_i.png', upload_to=upload_to_uuid('profile_image/profiles/'), blank=True)
    courses = models.ManyToManyField('home.Course',related_name='profiles')
    public = models.BooleanField(default=True, blank=True)
    saved_courses = models.ManyToManyField('home.Course',related_name='saved_courses')
    favorite_post_tags = models.ManyToManyField(Tag, related_name='fav_post_tags')
    favorite_buzz_tags = models.ManyToManyField(Tag, related_name='fav_buzz_tags')
    favorite_blog_tags = models.ManyToManyField(Tag, related_name='fav_blog_tags')
    recent_searches = models.ManyToManyField(SearchLog, related_name='recent_searches')
    
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

    def get_hashid(self):
        return hashids_user.encode(self.id)

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


