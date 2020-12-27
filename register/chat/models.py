from django.db import models
from main.models import Profile
from django.db.models import Q, F, Count, Avg, FloatField, Max, Min, Case, When
import uuid, secrets, math, io
from hashids import Hashids
from django.utils import timezone
from math import log
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
from django_uuid_upload import upload_to_uuid
import PIL
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile

hashid = Hashids(salt='9ejwb NOPHIqwpH9089h 0H9h130xPHJ io9wr',min_length=32)
hashid_messages = Hashids(salt='18BIOHBubi 23Ubliilb 89sevsdfuv wuboONEO3489',min_length=32)

class MessageManager(models.Manager):
    pass

class PrivateChatManager(models.Manager):
    
    def get_user_chats(self, user):
        
        ids = []
        time = content = ''
        last_message_content = {}
        try:
            qlookup = Q(user1=user) | Q(user2=user)
            qlookup2 = Q(user1=user) & Q(user2=user)
            qs = self.get_queryset().filter(qlookup).exclude(qlookup2).distinct().order_by('-messages__timestamp')
            for c in qs:
                last_message = c.get_last_message()
                if last_message != None:
                    time = last_message.get_time_sent_formatted()
                    content = last_message.contet
                if not c.user1 == user:
                    ids.append(c.user1.id)
                    last_message_content[c.user1.username] = { 'time':time, 'content':content }
                elif not c.user2 == user:
                    ids.append(c.user2.id)
                    last_message_content[c.user1.username] = { 'time':time, 'content':content }
                    last_message_content[c.user2.username] = { 'time':time, 'content':content }
            preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
            return Profile.objects.filter(id__in=ids).order_by(preserved), last_message_content
        except Exception as e:
            qlookup = Q(user1=user) | Q(user2=user)
            qs = self.get_queryset().filter(qlookup).distinct().order_by('-messages__timestamp')
            for c in qs:
                last_message = c.get_last_message()
                if last_message != None:
                    time = last_message.get_time_sent_formatted()
                    content = last_message.content
                if not c.user1 == user:
                    ids.append(c.user1.id)
                    last_message_content[c.user1.username] = { 'time': time, 'content':content }
                elif not c.user2 == user:
                    ids.append(c.user2.id)
                    last_message_content[c.user2.username] = { 'time':time, 'content':content }
            preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
            return Profile.objects.filter(id__in=ids).order_by(preserved), last_message_content
            
class PrivateChat(models.Model):
    guid = models.CharField(max_length=255,unique=True, null=True)
    user1 = models.ForeignKey(Profile, null=True, related_name='user1_room', on_delete=models.SET_NULL)
    user2 = models.ForeignKey(Profile, null=True, related_name='user2_room', on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True) 
    last_message = models.IntegerField(blank=True, null=True)
    
    objects = PrivateChatManager()
    
    def save(self, *args, **kwargs):      
        self.guid = secrets.token_hex(16)
        super(PrivateChat, self).save(*args, **kwargs)

    def get_hashid(self):
        return hashid.encode(self.guid)
    
    def get_messages(self, pre_connect_count=None, page=None):
        if page == None:
            messages = Message.objects.prefetch_related('author').filter(privatechat=self).order_by('-timestamp')[:15]
            if messages.count() < 1:
                messages = []
            has_messages = False if Message.objects.filter(privatechat=self).order_by('timestamp').first().id in [m.id for m in messages] else True
            return messages, has_messages
        else:
            messages_all = Message.objects.prefetch_related('author').filter(privatechat=self).order_by('-timestamp')[:pre_connect_count]
            page = page
            paginator = Paginator(messages_all, 15)
            try:
                messages = paginator.page(page)
            except PageNotAnInteger:
                messages = paginator.page(1)
            except EmptyPage:
                messages = paginator.page(paginator.num_pages)
            has_messages = False if Message.objects.filter(privatechat=self).order_by('timestamp').first().id in [m.id for m in messages] else True
            #messages, has_messages = Message.objects.filter(privatechat=self).order_by('timestamp')[pre_connect_count-page*15:pre_connect_count-(page-1)*15], Message.object.filter(privatechat=self).count() > page*15
            return messages, has_messages
        
    def set_last_message(self, message):
        self.last_message = message
        self.save()
    
    def get_messages_count(self):
        return Message.objects.filter(privatechat=self).count()
    
    def get_last_message(self):
        try:
            return Message.objects.filter(privatechat=self).order_by('-timestamp').first()
        except Exception as e:           
            print(e)
            return ''
    
    def get_first_message_time(self):
        try:
            return self.messages.order_by('timestamp').first().get_time_sent()
        except Exception as e:
            print(e)
            return ''
   
class Message(models.Model):
    author = models.ForeignKey(Profile, related_name='author_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    privatechat = models.ForeignKey(PrivateChat, related_name="messages", on_delete=models.DO_NOTHING)  
    replied = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name="replies")  
    is_image = models.BooleanField(null=True, default=False)
    photo = models.ImageField(upload_to=upload_to_uuid('messages/images/'), blank=True) 
    
    
    def save(self, *args, **kwargs):
        if (self.pk is None) and (len(str(self.photo))>0):
            print(self.photo)
            MAX_WIDTH = 1080
            MAX_HEIGHT = 1350
            img=Image.open(self.photo)
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
                img.save(output, format='JPEG', exif=exif, quality=76)
            else:
                img.save(output, format='JPEG', quality=76)
            output.seek(0)
            self.photo = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.photo.name, 'image/jpeg', output.getbuffer().nbytes, None)
        super(Message, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.author.username
    
    def get_hashid(self):
        return hashid_messages.encode(self.id)
    
    def get_time_sent(self):
        return str(self.timestamp)
    
    def get_author_hashed_id(self):
        return self.author.get_hashid()
    
    def get_author_full_name(self):
        return self.author.get_full_name()
    
    def get_replied_message(self):
        repliedTo = self.replied
        if repliedTo != None:
            return {
                "replied_content":repliedTo.content, 
                "replied_author":repliedTo.author.username, 
                "replied_author_fn":repliedTo.author.get_full_name(), 
                "replied_message_parent_author_firstname":repliedTo.author.first_name,
                }
        else: 
            return None
    
    def get_time_sent_formatted(self):
        now = timezone.now()
        diff= now - self.timestamp
        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds 
            return 'Now'  
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
    
    def is_image_message(self):
        is_image = True if self.is_image == True else False
        return is_image
    
    def get_photo_url(self):
        if self.is_image:
            return self.photo.url
        else:
            return None
        