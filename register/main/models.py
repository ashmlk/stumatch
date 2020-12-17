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
from django.contrib.auth.models import BaseUserManager, UserManager
from django.core.validators import MaxLengthValidator, MinValueValidator, MaxValueValidator
from django.db.models import Q, F, Count, Avg, FloatField
from hashids import Hashids
from friendship.models import Friend, Follow, Block, FriendshipRequest
from django.urls import reverse
from notifications.base.models import AbstractNotification
import time
from datetime import datetime

hashids_user = Hashids(salt='wvf935 vnw9py l-itkwnhe 3094',min_length=12)

hashids_notify  = Hashids(salt='2vbp W9PHh90H 2389V[H WOoksc',min_length=8)

hashid_user_chat = Hashids(salt='doubn 98354BGVBIWE obwKBN899rb wbIOWORK3',min_length=12)

#CUSTOM MODEL MANAGERS
class ProfileManager(UserManager):
    
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
                (Q(is_active=True)) &
                (Q(university__unaccent__icontains=university) & Q(program__unaccent__icontains=program)) |
                (Q(similarity_university__gte=0.8) & Q(similarity_program__gte=0.7)) |
                (Q(similarity_program__gte=0.85)) & 
                (Q(public=True)) 
            ).exclude(is_superuser=True).order_by('-similarity_university','-similarity_program')
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
                        (Q(is_active=True)) &
                        (Q(username__unaccent__trigram_similar=search_text) |
                        Q(last_name__unaccent__trigram_similar=search_text) |
                        Q(first_name__unaccent__trigram_similar=search_text) |
                        Q(username__unaccent__icontains=search_text)), trigram__gte=0.2
                    ).exclude(is_superuser=True).order_by('-trigram')
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
                    (Q(is_active=True)) &
                    (Q(rank__gte=0.3)|
                    Q(username__unaccent__trigram_similar=search_text) |
                    Q(last_name__unaccent__trigram_similar=search_text) |
                    Q(first_name__unaccent__trigram_similar=search_text)), trigram__gte=0.1
                ).exclude(is_superuser=True).order_by('-rank')[:5]
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
                    (Q(is_active=True)) &
                    (Q(username__unaccent__trigram_similar=search_text) |
                    Q(last_name__unaccent__trigram_similar=search_text) |
                    Q(first_name__unaccent__trigram_similar=search_text) |
                    Q(username__unaccent__icontains=search_text)), trigram__gte=0.03
                ).exclude(is_superuser=True).order_by('-trigram')
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
                (Q(is_active=True)) &
                (Q(rank__gte=0.2)|
                Q(username__unaccent__trigram_similar=search_text) |
                Q(last_name__unaccent__trigram_similar=search_text) |
                Q(first_name__unaccent__trigram_similar=search_text)), trigram__gte=0.03
            ).exclude(is_superuser=True).order_by('-rank')
        )
        
        return qs
        
    def get_students(self, user, code, instructor, instructor_fn, university):
        
        usernames = []
        blocked =  Block.objects.blocking(user)
        if blocked:
            for b in blocked:
                usernames.append(str(b))
        
        qs = (
            self.get_queryset()
            .filter(is_active=True, courses__course_code=code, courses__course_university__iexact=university, courses__course_instructor__iexact=instructor, courses__course_instructor_fn__iexact=instructor_fn)
            .exclude(username__in=usernames)
            .exclude(is_superuser=True)
            .order_by('last_name','first_name','university').distinct('last_name','first_name','university')
        )
        
        return qs
    
    def get_similar_friends(self, user):
        
        usernames = []
        
        user_courses = user.courses.all()
        friends = Friend.objects.friends(user)
        blocked =  Block.objects.blocking(user)
        
        if friends:
            for f in friends:
                usernames.append(str(f))
        if blocked:
            for b in blocked:
                usernames.append(str(b))
                
        qs = (
            self.get_queryset()
            .filter((Q(is_active=True)) & (Q(university=user.university) | Q(courses__course_code__in=[c.course_code for c in user_courses])))
            .exclude(username__in=usernames)
            .exclude(is_superuser=True)
            .order_by('last_name','first_name','university').distinct('last_name','first_name','university')
        )
        
        return qs
        
    def friends_with_courses(self, user, university):
        
        f_usernames = []
        friends = Friend.objects.friends(user)
        if friends:
            for f in friends:
                f_usernames.append(str(f))
        if university == '':
            if user.university:
                university = user.university
            else:
                return None
        qs = (
            self.get_queryset()
            .filter(is_active=True, username__in=f_usernames, university=university)
            .annotate(course_count=Count('courses'))
            .filter(course_count__gte=1)
            .order_by('last_name','first_name')
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
        

DEFAULT_IMAGE = 'defaults/user/default_u_i.png'
     
class Profile(AbstractUser):
    bio = models.TextField()
    university = models.CharField(max_length=50)
    program = models.CharField(null=True,blank=True,max_length=255)
    image = models.ImageField(default='defaults/user/default_u_i.png', upload_to=upload_to_uuid('profile_image/profiles/'), blank=True)
    courses = models.ManyToManyField('home.Course',related_name='profiles')
    public = models.BooleanField(default=True, blank=True)
    rank_objects = models.BooleanField(default=True, blank=True)
    save_searches = models.BooleanField(default=True, blank=True)
    saved_courses = models.ManyToManyField('home.Course',related_name='saved_courses')
    favorite_post_tags = models.ManyToManyField(Tag, related_name='fav_post_tags')
    favorite_buzz_tags = models.ManyToManyField(Tag, related_name='fav_buzz_tags')
    favorite_blog_tags = models.ManyToManyField(Tag, related_name='fav_blog_tags')
    recent_searches = models.ManyToManyField(SearchLog, related_name='recent_searches')
    # notification settings
    get_notify = models.BooleanField(default=True, blank=True)
    get_post_notify_all = models.BooleanField(default=True, blank=True)
    get_post_notify_likes = models.BooleanField(default=True, blank=True)
    get_post_notify_comments = models.BooleanField(default=True, blank=True)
    get_post_notify_mentions = models.BooleanField(default=True, blank=True)
    get_buzz_notify_all = models.BooleanField(default=True, blank=True)
    get_buzz_notify_likes = models.BooleanField(default=True, blank=True)
    get_buzz_notify_comments = models.BooleanField(default=True, blank=True)
    get_blog_notify_all = models.BooleanField(default=True, blank=True)
    get_blog_notify_likes = models.BooleanField(default=True, blank=True)
    get_blog_notify_comments = models.BooleanField(default=True, blank=True)
    get_friendrequest_notify = models.BooleanField(default=True, blank=True)
    get_friendrequestaccepted_notify = models.BooleanField(default=True, blank=True)
    
    sv = pg_search.SearchVectorField(null=True)
    
    objects = ProfileManager()
    
    class Meta:
        indexes = [
            GinIndex(fields=['sv'],name='search_idx_user'),
        ]
    
    def save(self, *args, **kwargs):
        self.username = self.username.lower()
        super(Profile, self).save(*args, **kwargs) 
        
    def __str__(self):
        return self.username
    
    def get_absolute_url(self):
        return reverse('main:get_user', kwargs={'username':self.username})

    def get_hashid(self):
        return hashids_user.encode(self.id)
    
    #remember to add back, this id is only for chat notifications
    def get_chat_hashid(self):
        return hashid_user_chat.encode(self.id)

    def set_image_to_default(self):
        if self.image.url != DEFAULT_IMAGE:
            self.image.delete(save=False)  # delete old image file
            self.image = DEFAULT_IMAGE
            self.save()
        else:
            self.image = DEFAULT_IMAGE
            self.save()

    def get_last_login_local(self):
        
        epoch = time.mktime(self.last_login.timetuple())
        offset = datetime.fromtimestamp (epoch) - datetime.utcfromtimestamp (epoch)
        return self.last_login + offset
    
    def get_date_joined_local(self):
        
        epoch = time.mktime(self.date_joined.timetuple())
        offset = datetime.fromtimestamp (epoch) - datetime.utcfromtimestamp (epoch)
        return self.date_joined + offset

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

class ReportBase(models.Model):
    class Meta:
        abstract = True
        
    class Reason(models.TextChoices):
        NOT_INTERESTED = 'not_interested', 'Not Interested in this content'
        SPAM = 'spam', 'It appears to be spam'
        SENSITIVE = 'sensitive', 'It displays sensitive content'
        HARMFUL = 'harmful', 'I find it abusive or harmful'
        SELF_HARM = 'self_harm', 'It displays and portrays expression of self-harm or suicide'
        HATE = 'hate', 'It appears to be inflammatory speech towards a demographic'
        MISLEADING = 'misleading', 'It appears to share misleading content'
        THREAT = 'threat', 'It is threatening and expressing violent harm'
    
    reporter = models.ForeignKey(Profile,on_delete=models.CASCADE)
    date_reported =  models.DateTimeField(auto_now_add=True)
    reason = models.CharField(
        max_length=250,
        choices=Reason.choices,
        default=Reason.NOT_INTERESTED
        )
    
    
class ReportUser(ReportBase):
    
    reported_obj = models.ForeignKey(Profile,on_delete=models.CASCADE, verbose_name='report_user', related_name='reported_users')
    
class ReportPost(ReportBase):
    
    reported_obj = models.ForeignKey('home.Post',on_delete=models.CASCADE, verbose_name='report_post', related_name='reported_posts')
    
class ReportComment(ReportBase):
    
    reported_obj = models.ForeignKey('home.Comment',on_delete=models.CASCADE, verbose_name='report_comment', related_name='reported_comments')
    
class ReportBuzz(ReportBase):
    
    reported_obj = models.ForeignKey('home.Buzz',on_delete=models.CASCADE, verbose_name='report_buzz', related_name='reported_buzzes')

class ReportBuzzReply(ReportBase):
    
    reported_obj = models.ForeignKey('home.BuzzReply',on_delete=models.CASCADE, verbose_name='report_buzzreply', related_name='reported_buzzreplies')
    
class ReportBlog(ReportBase):
    
    reported_obj = models.ForeignKey('home.Blog',on_delete=models.CASCADE, verbose_name='report_blog', related_name='reported_blogs')
    
class ReportBlogReply(ReportBase):
    
    reported_obj = models.ForeignKey('home.BlogReply',on_delete=models.CASCADE, verbose_name='report_blogreply', related_name='reported_blogreplies')
    
class ReportCourseReview(ReportBase):
    
    reported_obj = models.ForeignKey('home.Review',on_delete=models.CASCADE, verbose_name='report_coursereview', related_name='reported_coursereviews')

