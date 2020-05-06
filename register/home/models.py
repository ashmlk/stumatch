from django.db import models
from django.utils import timezone
from main.models import Profile
from django.urls import reverse
from django.core.validators import MaxLengthValidator, MinValueValidator, MaxValueValidator
from django.db.models import Q, F, Count
import uuid
import math
import secrets
from django_uuid_upload import upload_to_uuid
import uuid 
import datetime

def max_value_current_year():
    return datetime.date.today().year + 1

 
class Post(models.Model):
    title = models.CharField(max_length=100)
    guid_url = models.CharField(max_length=12,unique=True, null=True)
    content = models.TextField(validators=[MaxLengthValidator(1200)])
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)
    last_edited= models.DateTimeField(auto_now=True)
    likes= models.ManyToManyField(Profile, blank=True, related_name='post_likes')
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('home:post-detail')
    
    def user_liked(self, request):
        return self.likes.filter(id=request.user.id).exists()
    
    def save(self, *args, **kwargs):
        self.guid_url = secrets.token_urlsafe(8)
        super(Post, self).save(*args, **kwargs)
        
    def comment_count(self):
        comments = Comment.objects.filter(post=self, reply=None)
        return comments.count()
    
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
            months= math.floor(diff.days/30)       
            return str(months) + "m"
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
            months= math.floor(diff.days/30)       
            return str(months) + "m" + " ago "
        if diff.days >= 365:
            years= math.floor(diff.days/365)
            return str(years) + "y" + " ago "
            
def image_create_uuid_p_u(instance, filename):
    return '/'.join(['post_images', str(uuid.uuid4().hex + ".png")]) 
        
class Images(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='images')
    image = models.FileField(upload_to=upload_to_uuid('media/post_images/'),verbose_name='Image')
    date_added = models.DateTimeField(auto_now_add=True)
    
class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.ForeignKey(Profile, on_delete=models.CASCADE)
    body = models.TextField()
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
    
    def get_created_on(self):
        now = timezone.now()
        diff= now - self.created_on
        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds 
            if seconds == 1:
                return str(seconds) +  "s"
            else:
                return str(seconds) + " s"     
        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)
            if minutes == 1:
                return str(minutes) + "m" 
            else:
                return str(minutes) + "m"
        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)
            if hours == 1:
                return str(hours) + "h"
            else:
                return str(hours) + "h"
        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
            if days == 1:
                return str(days) + "d"
            else:
                return str(days) + "d"
        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)       
            if months == 1:
                return str(months) + "m"
            else:
                return str(months) + "m"
        if diff.days >= 365:
            years= math.floor(diff.days/365)
            if years == 1:
                return str(years) + "y"
            else:
                return str(years) + "y"
    def get_uuid(self):
        return str(uuid.uuid4()) 

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
    course_instructor = models.CharField(max_length=100)
    is_shared = models.BooleanField(default=False)
    course_year = models.IntegerField(('year'), validators=[MinValueValidator(1984), MaxValueValidator(max_value_current_year())])
    course_likes = models.ManyToManyField(Profile, blank=True, related_name='course_likes')
    course_dislikes = models.ManyToManyField(Profile, blank=True, related_name='course_dislikes')
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
    def __str__(self):
        return self.course_code
    
    def save(self, *args, **kwargs):
        self.course_code = self.course_code.upper().replace(' ', '')
        self.course_university = self.course_university.strip().lower().replace('university','')
        self.course_instructor = self.course_instructor.strip().lower()
        super(Course, self).save(*args, **kwargs)    
    
    def get_course_university(self):
        if 'university' in self.course_university:
            return self.course_university.capitalize().replace('university', 'University')
        else:
            return self.course_university.capitalize() + 'University'
    
    def get_user_count(self):
        courses = Course.objects.filter(course_code=self.course_code,course_university=self.course_university)
        num = 0
        for c in courses:
            num += c.profiles.count()
        return num
    
    def get_user_count_ins(self):
        courses = Course.objects.filter(course_code=self.course_code,course_university=self.course_university,course_instructor=self.course_instructor)
        num = 0
        for c in courses:
            num += c.profiles.count()
        return num
    
    def average_voting(self):
        total_likes = Course.course_likes.through.objects.filter(course__course_code=self.course_code,course__course_university=self.course_university,course__course_instructor=self.course_instructor).count()
        total_dislikes = Course.course_dislikes.through.objects.filter(course__course_code=self.course_code,course__course_university=self.course_university,course__course_instructor=self.course_instructor).count()
        t = total_likes - total_dislikes
        t = float('{:.3g}'.format(t))
        magnitude = 0
        while abs(t) >= 1000:
            magnitude += 1
            t /= 1000.0
        return '{}{}'.format('{:f}'.format(t).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])
    
    def average_voting_ins(self):
        total_likes = Course.objects.filter(course_code=self.course_code,course_university=self.course_university,course_instructor=self.course_instructor).course_likes.count()
        total_dislikes = Course.objects.filter(course_code=self.course_code,course_university=self.course_university,course_instructor=self.course_instructor).course_dislikes.count()
        t = total_likes - total_dislikes
        t = float('{:.3g}'.format(t))
        magnitude = 0
        while abs(t) >= 1000:
            magnitude += 1
            t /= 1000.0
        return '{}{}'.format('{:f}'.format(t).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])
    
    def sem(self):      
        r_dic = {1:"Spring",2:"Summer",3:"Fall",4:"Winter"}
        d = int(self.course_difficulty)
        return r_dic[d]
        
    def average_complexity(self):
        r_dic = {1:"Easy",2:"Medium",3:"Hard",4:"Most Failed"}
        courses = Course.objects.filter(course_code=self.course_code,course_university=self.course_university)
        avg_cplx = 0
        total_courses = courses.count()
        complexity_sum = 0
        for c in courses:
            complexity_sum += int(c.course_difficulty)
        avg_cplx = round(complexity_sum / total_courses)
        return r_dic[avg_cplx]
    
    def user_complexity(self):
        r_dic = {1:"Easy",2:"Medium",3:"Hard",4:"a Failure"}
        return r_dic[int(self.course_difficulty)]
        
    def average_complexity_ins(self):
        r_dic = {1:"Easy",2:"Medium",3:"Hard",4:"Most Failed"}
        courses = Course.objects.filter(course_code=self.course_code,course_university=self.course_university,course_instructor=self.course_instructor)
        avg_cplx = 0
        total_courses = courses.count()
        complexity_sum = 0
        for c in courses:
            complexity_sum += int(c.course_difficulty)
        avg_cplx = round(complexity_sum / total_courses)
        return r_dic[avg_cplx]
    
    def is_liked(self,user):
        return Course.course_likes.through.objects.filter(course__course_code=self.course_code,course__course_university=self.course_university,course__course_instructor=self.course_instructor,profile_id=user.id).exists()
    
    def not_liked(self,user):
        return Course.course_dislikes.through.objects.filter(course__course_code=self.course_code,course__course_university=self.course_university,course__course_instructor=self.course_instructor,profile_id=user.id).exists()
    
    


        
        

        
        