from django.db import models
from main.models import Profile
import uuid
from hashids import Hashids

hashid = Hashids(salt='9ejwb NOPHIqwpH9089h 0H9h130xPHJ iojpf909wrwas',min_length=32)

class MessageManager(models.Manager):
    pass

class PrivateChatManager(models.Manager):
    
    def get_user_chats(self, user):
        
        try:
            qlookup = Q(user1=user) | Q(user2=user)
            qlookup2 = Q(user1=user) | Q(user2=user)
            qs = self.get_queryset().filter(qlookup).exclude(qlookup2).distinct()
        except Exception as e:
            qs = self.get_queryset().filter(qlookup).distinct()
            
        
    

class PrivateChat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user1 = models.ForeignKey(Profile, null=True, related_name='user1_room', on_delete=models.SET_NULL)
    user2 = models.ForeignKey(Profile, null=True, related_name='user2_room', on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def get_hashid(self):
        return hashid.encode(self.id)    

class Message(models.Model):
    author = models.ForeignKey(Profile, related_name='author_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    privatechat = models.ForeignKey(PrivateChat, blank=False, null=False, related_name="messages", on_delete=models.CASCADE)
    
    def __str__(self):
        return self.author.username
    