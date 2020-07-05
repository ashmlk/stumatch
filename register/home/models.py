from django.db import models
from django.utils import timezone
from main.models import Profile, BookmarkPost, BookmarkBlog, BookmarkBuzz
from django.urls import reverse
from django.core.validators import MaxLengthValidator, MinValueValidator, MaxValueValidator
from django.db.models import Q, F, Count, Avg, FloatField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.functions import Cast
from django.template.defaultfilters import slugify
import uuid
import math
import secrets
from django_uuid_upload import upload_to_uuid
import uuid 
import datetime
from math import log
import pytz
from dateutil import tz
import PIL
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
import io
from hashids import Hashids
from ckeditor_uploader.fields import RichTextUploadingField
import readtime
from taggit_selectize.managers import TaggableManager
from django.contrib.postgres.search import (SearchQuery, SearchRank, SearchVector, TrigramSimilarity,)
from django.contrib.postgres.aggregates import StringAgg
from django.contrib.postgres.indexes import GinIndex
import django.contrib.postgres.search as pg_search
from django.db.models.functions import Greatest
from stream_django.activity import Activity

#CUSTOM MODEL MANAGERS
class PostManager(models.Manager):
    
    def search_topresult(self, search_text):
        
        search_vectors = ( 
              SearchVector(
                  'title', weight='A', config='english'
            
                ) + SearchVector(
                    StringAgg('content', delimiter=' '),
                    weight='B', config='english'
                )
              )
        search_query = SearchQuery(
            search_text, config='english'
        )
        search_rank = SearchRank(search_vectors,search_query)
        trigram = (TrigramSimilarity(
            'title', search_text
        ) + (TrigramSimilarity(
            'content', search_text
        ))
        )
        qs = (
            self.get_queryset()
            .filter(sv=search_query)
            .annotate(rank=search_rank, trigram=trigram, bs=Greatest('rank','trigram'))
            .filter(Q(bs__gte=0.2))
            .order_by('-bs')[:5]
        )
        if qs.count() < 1:
                return self.search(search_text)[:5]
        else:
                return qs
        
    def search(self, search_text):
        search_vectors = ( 
              SearchVector(
                  'title', weight='A', config='english'
            
                ) + SearchVector(
                    StringAgg('content', delimiter=' '),
                    weight='B', config='english'
                )
              )
        search_query = SearchQuery(
            search_text, config='english'
        )
        search_rank = SearchRank(search_vectors,search_query)
        trigram = (TrigramSimilarity(
            'title', search_text
        ) + (TrigramSimilarity(
            'content', search_text
        ))
        )
        qs = (
            self.get_queryset()
            .filter(sv=search_query)
            .annotate(rank=search_rank, trigram=trigram, bs=Greatest('rank','trigram'))
            .filter(Q(bs__gte=0.1))
            .order_by('-bs')
        )
        
        return qs
    
    
    def get_hot(self,user):
        
        qs = (
            self.get_queryset()
            .select_related("author")
            .exclude(author=user)
        )
        
        qs_list = list(qs)
        sorted_post = sorted(qs_list, key=lambda p: p.hot(), reverse=True)
        
        return sorted_post
        
        
        
        
class BlogManager(models.Manager):
    
    def search_topresult(self, search_text):
    
        search_vectors = ( 
              SearchVector(
                  'title', weight='A', config='english'
            
                ) + SearchVector(
                    StringAgg('content', delimiter=' '),
                    weight='B', config='english'
                )
              )
        search_query = SearchQuery(
            search_text, config='english'
        )
        search_rank = SearchRank(search_vectors,search_query)
        trigram = (TrigramSimilarity(
            'title', search_text
            )
        )
        
        qs = (
            self.get_queryset()
            .filter(sv=search_query)
            .annotate(rank=search_rank, trigram=trigram, bs=Greatest('rank','trigram'))
            .filter(Q(bs__gte=0.2))
            .order_by('-bs')[:5]
        )
        if qs.count() < 1:
                return self.search(search_text)[:5]
        else:
                return qs
             
             
    
    def search(self, search_text):
        search_vectors = ( 
              SearchVector(
                  'title', weight='A', config='english'
            
                ) + SearchVector(
                    StringAgg('content', delimiter=' '),
                    weight='B', config='english'
                )
              )
        search_query = SearchQuery(
            search_text, config='english'
        )
        search_rank = SearchRank(search_vectors,search_query)
        trigram = (TrigramSimilarity(
            'title',search_text
        ))
        
        qs = (
            self.get_queryset()
            .filter(sv=search_query)
            .annotate(rank=search_rank, trigram=trigram, bs=Greatest('rank','trigram'))
            .filter(Q(bs__gte=0.05))
            .order_by('-bs')
        )
        
        return qs

class BuzzManager(models.Manager):
    
    def search_topresult(self, search_text):
        
        search_vectors = ( 
              SearchVector(
                  'title', weight='A', config='english'
            
                ) + SearchVector(
                    StringAgg('content', delimiter=' '),
                    weight='B', config='english'
                )
              )
        search_query = SearchQuery(
            search_text, config='english'
        )
        search_rank = SearchRank(search_vectors,search_query)
        trigram = (TrigramSimilarity(
            'title', search_text
        ) + (TrigramSimilarity(
            'content', search_text
        ))
        )
        qs = (
            self.get_queryset()
            .filter(sv=search_query)
            .annotate(rank=search_rank, trigram=trigram, bs=Greatest('rank','trigram'))
            .filter(Q(bs__gte=0.2))
            .order_by('-bs')[:5]
        )
        if qs.count() < 1:
                return self.search(search_text)[:5]
        else:
                return qs
            
             
    
    def search(self, search_text):
        search_vectors = ( 
              SearchVector(
                  'title', weight='A', config='english'
            
                ) + SearchVector(
                    StringAgg('content', delimiter=' '),
                    weight='B', config='english'
                ) + SearchVector(
                    'nickname', weight='C', config='english'
                )
              )
        search_query = SearchQuery(
            search_text, config='english'
        )
        search_rank = SearchRank(search_vectors,search_query)
        trigram = (TrigramSimilarity(
            'title', search_text
        ) + TrigramSimilarity(
            'nickname', search_text
        ))
        
        qs = (
            self.get_queryset()
            .filter(sv=search_query)
            .annotate(rank=search_rank, trigram=trigram, bs=Greatest('rank','trigram'))
            .filter(Q(bs__gte=0.05))
            .order_by('-bs')
        )
        
        return qs


class CourseManager(models.Manager):
    
    def search(self, search_text):
        
        search_vectors = ( 
              SearchVector(
                  'course_code', weight='A', config='english'
            
                ) + SearchVector(
                    'course_instructor', deweight='C', config='english'
                    
                ) + SearchVector(
                    StringAgg('course_university', delimiter=' '),
                    weight='C', config='english'
                    
                ) + SearchVector(
                    'course_code','course_instructor', weight='B', config='english'
                    
                ) + SearchVector(
                    'course_university','course_instructor', weight='B', config='english'
                )
                
              )
        search_query = SearchQuery(
            search_text, config='english'
        )
        search_rank = SearchRank(search_vectors,search_query)
        
        trigram = (TrigramSimilarity(
            'course_code', search_text
            ) + TrigramSimilarity(
                'course_instructor', search_text
            ) + TrigramSimilarity(
                'course_university', search_text
            ) 
        )
        
        ds = self.get_queryset().distinct('course_code','course_instructor','course_university')
        
        qs = (
            self.get_queryset()
            .annotate(rank=search_rank, trigram=trigram, bs=Greatest('trigram','rank'))
            .filter(
                Q(rank__gte=0.2)|
                Q(trigram__gte=0.09)|
                Q(course_code__unaccent__trigram_similar=search_text) 
            )
            .filter(id__in=ds).order_by('-bs')
        )
        
        return qs
    
    
    

hashids = Hashids(salt='v2ga hoei232q3r prb23lqep weprhza9',min_length=8)

def max_value_current_year():
    return datetime.date.today().year + 1
 
class Post(models.Model, Activity):
    title = models.CharField(max_length=100)
    guid_url = models.CharField(max_length=255,unique=True, null=True)
    content = models.TextField(validators=[MaxLengthValidator(1200)])
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)
    last_edited= models.DateTimeField(auto_now=True)
    tags = TaggableManager(help_text="Tags", blank=True)
    likes= models.ManyToManyField(Profile, blank=True, related_name='post_likes')
    sv = pg_search.SearchVectorField(null=True)
    
    objects = PostManager()
    
    class Meta:
        indexes = [
            GinIndex(fields=['sv'],name='search_idx_post'),
        ]
           
    def __str__(self):
        return self.title

    def get_hashid(self):
        return hashids.encode(self.id)
    
    def get_absolute_url(self):
        return reverse('home:post-detail')
    
    def user_liked(self, request):
        return self.likes.filter(id=request.user.id).exists()
    
    def save(self, *args, **kwargs):
        self.guid_url = secrets.token_urlsafe(8)
        super(Post, self).save(*args, **kwargs)
        
    def comment_count(self):
        return self.comments.filter(post=self, reply=None).count()
    
    def image_count_as_list(self):
        c = self.images.count()
        return range(0,c)

    def get_created_on(self):
        now = timezone.now()
        diff= now - self.date_posted
        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds 
            return 'Just now'  
        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)
            return str(minutes) + "m"
        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)
            return str(hours) + "h"
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
            return str(days) + "d"
        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/7)       
            return str(months) + "w"
        if diff.days >= 365:
            years= math.floor(diff.days/365)
            return str(years) + "y"
        
    def has_image(self):
        if self.images.count() > 0:
            return True
        else:
            return False
        
    def edited(self):
        if (self.last_edited - self.date_posted).seconds > 1800:
            return True 
          
    def get_edited_on(self):
        now = timezone.now()
        diff= now - self.last_edited
        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds 
            return 'Just now'  
        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)
            return str(minutes) + "m" + " ago "
        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)
            return str(hours) + "h" + " ago "
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
            return str(days) + "d" + " ago "
        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/7)       
            return str(months) + "w" + " ago "
        if diff.days >= 365:
            years= math.floor(diff.days/365)
            return str(years) + "y" + " ago "
    
    epoch = datetime.datetime(1970, 1, 1)
    
    def epoch_seconds(date):
        td = date - epoch
        return td.days * 86400 + td.seconds + (float(td.microseconds) / 1000000)

    def score(comments, likes):
        
        # comments recieve constant factor of 1.8
        1.8 * comments + likes
    
    def hot(self):
        
        comments = self.comments.count()
        likes = self.likes.count()
        date = self.last_edited
        
        score = score(comments, likes)
        z = log(max(abs(score), 1), 10)
        y = 1 if score > 0 else -1 if score < 0 else 0
        seconds = epoch_seconds(date) - 1134028003
        return round(y * z + seconds / 45000, 7)
            
def image_create_uuid_p_u(instance, filename):
    return '/'.join(['post_images', str(uuid.uuid4().hex + ".png")]) 
        
class Images(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='images')
    image = models.FileField(upload_to=upload_to_uuid('media/post_images/'),verbose_name='Image')
    date_added = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        
        if self.pk is None:
            MAX_WIDTH = 1080
            MAX_HEIGHT = 1350
            img=Image.open(self.image)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            exif = None
            if 'exif' in img.info:
                exif=img.info['exif']
            ratio = min(MAX_WIDTH/img.size[0], MAX_HEIGHT/img.size[1])
            if img.size[0] > MAX_WIDTH or img.size[1] > MAX_HEIGHT:
                img = img.resize((int(img.size[0]*ratio), int(img.size[1]*ratio)), PIL.Image.ANTIALIAS)
            else:
                img = img.resize((img.size[0], img.size[1]), PIL.Image.ANTIALIAS)
            output = io.BytesIO()
            if exif:
                img.save(output, format='JPEG', exif=exif, quality=90)
            else:
                img.save(output, format='JPEG', quality=90)
            output.seek(0)
            self.image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.image.name, 'image/jpeg', output.getbuffer().nbytes, None)
            super(Images, self).save(*args, **kwargs)
            
class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.ForeignKey(Profile, on_delete=models.CASCADE)
    body = models.TextField(validators=[MaxLengthValidator(350)])
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name="replies")
    likes= models.ManyToManyField(Profile, blank=True, related_name='comment_likes')

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)
    
    def likes_count(self):
        return self.likes.count()
    
    def get_hashid(self):
        return hashids.encode(self.id)
    
    def get_created_on(self):
        now = timezone.now()
        diff= now - self.created_on
        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds 
            return str(seconds) + " s"     
        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)
            return str(minutes) + "m"
        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)
            return str(hours) + "h"
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
            return str(days) + "d"
        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/7)       
            return str(months) + "w"
        if diff.days >= 365:
            years= math.floor(diff.days/365)
            return str(years) + "y"
        
    def get_uuid(self):
        return str(uuid.uuid4()) 

class Review(models.Model):
    class Interesting(models.TextChoices):
        INTERESTING = '1', 'Interesting'
        RELATIVELY = '2', 'Relatively Interesting'
        NOT = '3', 'Not Interesting'
        NO_OPINION = '4', 'No opinion'
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    body = models.TextField(validators=[MaxLengthValidator(400)])
    created_on = models.DateTimeField(auto_now_add=True)
    likes= models.ManyToManyField(Profile, blank=True, related_name='review_likes')
    dislikes= models.ManyToManyField(Profile, blank=True, related_name='review_dislikes')
    review_interest = models.CharField(
        max_length=2,
        choices=Interesting.choices,
        default=Interesting.NO_OPINION
        )
    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return 'Review {} by {}'.format(self.body, self.author.get_username)
    
    def get_hashid(self):
        return hashids.encode(self.id)

    def get_created_on(self):
        now = timezone.now()
        diff= now - self.created_on
        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds 
            return str(seconds) + " s"     
        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)
            return str(minutes) + "m"
        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)            
            return str(hours) + "h"
        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days          
            return str(days) + "d"
        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)                
            return str(months) + "m"
        if diff.days >= 365:
            years= math.floor(diff.days/365)            
            return str(years) + "y"
        
    def get_course_prof(self):
        return Course.objects.get(course_reviews__id=self.id).course_instructor
    
    def get_course_yr(self):
        return Course.objects.get(course_reviews__id=self.id).course_year
    
    def get_course_sm(self):
        return Course.objects.get(course_reviews__id=self.id).sem()
    
class Course(models.Model):
    
    class Semester(models.TextChoices):
        SPRING = '1', 'Spring'
        SUMMER = '2', 'Summer'
        FALL = '3', 'Fall'
        WINTER = '4', 'Winter'
        NONE = '0', 'None'
    class Difficulty(models.TextChoices):
        EASY = '1', 'Easy'
        MEDIUM = '2', 'Medium'
        HARD = '3', 'Hard'
        FAILED = '4', 'Failed'
    course_code = models.CharField(max_length=20)
    course_university = models.CharField(max_length=100)
    course_university_slug = models.SlugField(max_length = 250, null = True, blank = True)
    course_instructor_slug = models.SlugField(max_length = 250, null = True, blank = True)
    course_instructor = models.CharField(max_length=100)
    course_year = models.IntegerField(('year'), validators=[MinValueValidator(1984), MaxValueValidator(max_value_current_year())])
    course_likes = models.ManyToManyField(Profile, blank=True, related_name='course_likes')
    course_dislikes = models.ManyToManyField(Profile, blank=True, related_name='course_dislikes')
    course_reviews = models.ManyToManyField(Review, blank=True, related_name='course_reviews')
    course_semester = models.CharField(
        max_length=2,
        choices=Semester.choices,
        default=Semester.NONE
        )
    course_difficulty = models.CharField(
        max_length=2,
        choices=Difficulty.choices,
        default=Difficulty.MEDIUM
        )
    sv = pg_search.SearchVectorField(null=True)
    
    objects = CourseManager()
    
    class Meta:
        indexes = [
            GinIndex(fields=['sv'],name='search_idx_course'),
        ]
    def __str__(self):
        return self.course_code
    
    def save(self, *args, **kwargs):
        self.course_code = self.course_code.upper().replace(' ', '')
        self.course_university_slug = slugify(self.course_university.strip().lower())
        self.course_instructor_slug = slugify(self.course_instructor.strip().lower())
        super(Course, self).save(*args, **kwargs)   
        
    def get_hashid(self):
        return hashids.encode(self.id)
    
    def get_user_count(self):
        courses = Course.objects.filter(course_code=self.course_code,course_university__iexact=self.course_university).annotate(user_count=Count('profiles'))
        return courses[0].user_count
    
    def get_user_count_ins(self):
        courses = Course.objects.filter(course_code=self.course_code,course_university__iexact=self.course_university,course_instructor__iexact=self.course_instructor)\
            .annotate(user_count=Count('profiles'))
        return courses[0].user_count
    
    def average_voting(self):
        total_likes = Course.course_likes.through.objects.filter(course__course_code=self.course_code,course__course_university__iexact=self.course_university,\
            course__course_instructor=self.course_instructor).count()
        total_dislikes = Course.course_dislikes.through.objects.filter(course__course_code=self.course_code,course__course_university__iexact=self.course_university,\
            course__course_instructor__iexact=self.course_instructor).count()
        t = total_likes - total_dislikes
        if t==0:
            return "Rate"
        t = float('{:.3g}'.format(t))
        magnitude = 0
        while abs(t) >= 1000:
            magnitude += 1
            t /= 1000.0
        return '{}{}'.format('{:f}'.format(t).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])
    
    def average_voting_ins(self):
        total_likes = Course.objects.filter(course_code=self.course_code,course_university__iexact=self.course_university,\
            course_instructor=self.course_instructor).course_likes.count()
        total_dislikes = Course.objects.filter(course_code=self.course_code,course_university__iexact=self.course_university,\
            course_instructor__iexact=self.course_instructor).course_dislikes.count()
        t = total_likes - total_dislikes
        t = float('{:.3g}'.format(t))
        magnitude = 0
        while abs(t) >= 1000:
            magnitude += 1
            t /= 1000.0
        return '{}{}'.format('{:f}'.format(t).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])
    
    def complexity_btn(self):
        r_dic = {"Easy":"success","Medium":"warning","Hard":"danger","Most Failed":"dark"}
        return (r_dic[self.average_complexity()])
    
    def complexity_btn_ins(self):
        r_dic = {"Easy":"success","Medium":"warning","Hard":"danger","Most Failed":"dark"}
        return (r_dic[self.average_complexity_ins()])
    
    def sem(self):      
        r_dic = {1:"Spring",2:"Summer",3:"Fall",4:"Winter"}
        d = int(self.course_difficulty)
        return r_dic[d]
        
    def average_complexity(self):
        r_dic = {1:"Easy",2:"Medium",3:"Hard",4:"Most Failed"}
        avg = Course.objects.filter(course_code=self.course_code,course_university__iexact=self.course_university).\
            annotate(as_float=Cast('course_difficulty',FloatField())).aggregate(Avg('as_float'))
        return r_dic[int(avg.get('as_float__avg'))]
    
    def average_complexity_ins(self):
        r_dic = {1:"Easy",2:"Medium",3:"Hard",4:"Most Failed"}
        avg = Course.objects.filter(course_code=self.course_code,course_university__iexact=self.course_university,\
            course_instructor__iexact=self.course_instructor).annotate(as_float=Cast('course_difficulty',FloatField())).aggregate(Avg('as_float'))
        return r_dic[int(avg.get('as_float__avg'))]
    
    def user_complexity(self):
        r_dic = {1:"easy",2:"medium",3:"hard",4:"a failure"}
        return r_dic[int(self.course_difficulty)]
    
    def user_complexity_btn(self):
        r_dic = {1:"Easy",2:"Medium",3:"Hard",4:"Most Failed"}
        return r_dic[int(self.course_difficulty)]
    
    def is_liked(self,user):
        return Course.course_likes.through.objects.filter(course__course_code=self.course_code,\
            course__course_university__iexact=self.course_university,course__course_instructor__iexact=self.course_instructor,profile_id=user.id).exists()
    
    def not_liked(self,user):
        return Course.course_dislikes.through.objects.filter(course__course_code=self.course_code,\
            course__course_university__iexact=self.course_university,course__course_instructor__iexact=self.course_instructor,profile_id=user.id).exists()
    
    def get_reviews(self):
        return Review.objects.filter(course_reviews__course_code=self.course_code,\
            course_reviews__course_instructor__iexact=self.course_instructor,course_reviews__course_university__iexact=self.course_university).distinct()
    
    def get_reviews_all(self):
       return Review.objects.filter(course_reviews__course_code=self.course_code,\
           course_reviews__course_university__iexact=self.course_university).distinct()
    
    def reviews_count(self):
       return Course.course_reviews.through.objects.filter(course__course_code=self.course_code,\
           course__course_university__iexact=self.course_university,course__course_instructor__iexact=self.course_instructor).count()
    
    def reviews_all_count(self):
       return Course.course_reviews.through.objects.filter(course__course_code=self.course_code,\
           course__course_university__iexact=self.course_university).count()
    
class Buzz(models.Model, Activity):
    nickname = models.CharField(max_length=30, blank=True, null = True)
    title = models.CharField(max_length=90)
    guid_url = models.CharField(max_length=255,unique=True)
    content = models.TextField(validators=[MaxLengthValidator(550)])
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)
    last_edited= models.DateTimeField(auto_now=True)
    expiry = models.DateTimeField(blank=True, null=True)
    tags = TaggableManager(help_text="Tags", blank=True)
    likes= models.ManyToManyField(Profile, blank=True, related_name='likes')
    dislikes= models.ManyToManyField(Profile, blank=True, related_name='dilikes')
    wots= models.ManyToManyField(Profile, blank=True, related_name='wots')
    shares = models.ManyToManyField(Profile, blank=True, related_name='shares')
    sv = pg_search.SearchVectorField(null=True)
    
    objects = BuzzManager()
    
    class Meta:
        indexes = [
            GinIndex(fields=['sv'],name='search_idx_buzz'),
        ]
        
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.guid_url = secrets.token_urlsafe(12)
        super(Buzz, self).save(*args, **kwargs) 
    
    def get_hashid(self):
        return hashids.encode(self.id)
    
    def get_created_on(self):
        now = timezone.now()
        diff= now - self.date_posted
        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds 
            return 'Just now'  
        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)
            return str(minutes) + "m"
        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)
            return str(hours) + "h"
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
            return str(days) + "d"
        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/7)       
            return str(months) + "w"
        if diff.days >= 365:
            years= math.floor(diff.days/365)
            return str(years) + "y"
    
    def get_expiry(self):
        if self.expiry is not None:
            now = timezone.now()
            if self.expiry > now:
                diff = self.expiry - now
                if diff.seconds >= 3600 and diff.days < 1:
                    hours= math.floor(diff.seconds/3600)
                    return "expirying in " + str(hours) + "h"
                if diff.days >= 1 and diff.days < 30:
                    days = diff.days
                    return "expirying in " + str(days) + "d"
            else: 
                diff = now - self.expiry
                if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
                    seconds= diff.seconds 
                    return 'Just expired'  
                if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
                    minutes= math.floor(diff.seconds/60)
                    return "expired " + str(minutes) + "m" + " ago"
                if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
                    hours= math.floor(diff.seconds/3600)
                    return "expired " + str(hours) + "h" + " ago"
                if diff.days >= 1 and diff.days < 30:
                    days= diff.days
                    return "expired " + str(days) + "d" + " ago"
                if diff.days >= 30 and diff.days < 365:
                    months= math.floor(diff.days/7)       
                    return "expired " + str(months) + "w" + " ago"
                if diff.days >= 365:
                    years= math.floor(diff.days/365)
                    return "expired " + str(years) + "y" + " ago"
                

class BuzzReply(models.Model):
    
    buzz = models.ForeignKey(Buzz,on_delete=models.CASCADE,related_name='breplies')
    reply_nickname = models.CharField(max_length=30, blank=True, null = True)
    reply_content = models.TextField(validators=[MaxLengthValidator(180)])
    reply_author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date_replied = models.DateTimeField(auto_now_add=True)
    reply_likes= models.ManyToManyField(Profile, blank=True, related_name='rlikes')
    reply_dislikes= models.ManyToManyField(Profile, blank=True, related_name='rdislikes')
    
    def __str__(self):
        return self.reply_nickname
    
    def get_hashid(self):
        return hashids.encode(self.id)
    
    def get_created_on(self):
        now = timezone.now()
        diff= now - self.date_replied
        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds 
            return 'Just now'  
        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)
            return str(minutes) + "m"
        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)
            return str(hours) + "h"
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
            return str(days) + "d"
        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/7)       
            return str(months) + "w"
        if diff.days >= 365:
            years= math.floor(diff.days/365)
            return str(years) + "y"
    
class Blog(models.Model):
    
    title = models.CharField(max_length=200)
    guid_url = models.CharField(max_length=255,unique=True)
    content = RichTextUploadingField(blank=True,null=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)
    last_edited= models.DateTimeField(auto_now=True)
    tags = TaggableManager(help_text="Tags", blank=True)
    slug = models.SlugField(null = True, blank = True)
    likes= models.ManyToManyField(Profile, blank=True, related_name='blog_likes')
    sv = pg_search.SearchVectorField(null=True)
    
    objects = BlogManager()
    
    class Meta:
        indexes = [
            GinIndex(fields=['sv'],name='search_idx_blog'),
        ]  
        
    def save(self, *args, **kwargs):
        self.guid_url = secrets.token_urlsafe(6)
        self.title = self.title.strip()
        self.slug = slugify(self.title.strip().lower())
        super(Blog, self).save(*args, **kwargs)
         
    def get_hashid(self):
        return hashids.encode(self.id)
    
    def get_readtime(self):
        result = readtime.of_text(str(self.content))
        result = round(result.seconds / 60)
        if result <= 1:
            return '1 min'
        else:
            return str(result) + ' min'

class BlogReply(models.Model):
    
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE,related_name='blog_replies')
    content = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date_replied = models.DateTimeField(auto_now_add=True)
    reply_likes= models.ManyToManyField(Profile, blank=True, related_name='brlikes')

    def __str__(self):
        return self.reply_nickname
    
    def get_hashid(self):
        return hashids.encode(self.id)
    
    def get_created_on(self):
        now = timezone.now()
        diff= now - self.date_replied
        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds 
            return 'Just now'  
        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)
            return str(minutes) + "m"
        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)
            return str(hours) + "h"
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
            return str(days) + "d"
        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/7)       
            return str(months) + "w"
        if diff.days >= 365:
            years= math.floor(diff.days/365)
            return str(years) + "y"
    
            
        