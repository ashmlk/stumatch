from asgiref.sync import async_to_sync
import json
from channels.generic.websocket import WebsocketConsumer
from .models import Message, PrivateChat
from main.models import Profile
from django.db.models import Q
from hashids import Hashids
import math
from channels.db import database_sync_to_async

hashid = Hashids(salt='9ejwb NOPHIqwpH9089h 0H9h130xPHJ iojpf909wrwas',min_length=32)

class ChatConsumer(WebsocketConsumer):
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.room = None
        self.messages_pre_connect_count = None
        self.last_message = None
        self.page = 1
        self.last_message_id = None
        
    def fetch_messages(self, data):
        room = PrivateChat.objects.get(guid=data['room_id'])
        messages = room.get_messages()
        result = []
        for message in messages:
            json_message =  {
                'id':message.id,
                'author':message.author.username,
                'content':message.content,
                'timestamp':str(message.get_time_sent),
            }
            result.append(json_message)
        content = {
            'command':'messages',
            'messages': result
        }
        self.send_chat_message(content)
        
    def load_messages(self, data):
        room = PrivateChat.objects.get(guid=data['room_id'])
        messages = room.get_messages(pre_connect_count=self.messages_pre_connect_count,page=self.page+1)
        self.page+=1
        result = []
        for message in messages:
            json_message =  {
            'id':message.id,
            'author':message.author.username,
            'content':message.content,
            'timestamp':str(message.get_time_sent),
            }
            result.append(json_message)
        content = {
            'command':'messages',
            'messages': result
        }
        self.send_chat_message(content) 
        
    def new_message(self, data):
        author = data['from']
        author_user = Profile.objects.get(username=author)
        message = Message.objects.create(
                author=author_user,
                content=data['message'],
                privatechat = self.room
            )
        self.last_message = message
        self.last_message_id = message.id
        json_message =  {
            'id':message.id,
            'author':message.author.username,
            'content':message.content,
            'timestamp':str(message.get_time_sent),
            'last_message_content':self.last_message.content,
            'last_message_time':self.last_message.get_time_sent()
            }
        content = {
            'command':'new_message',
            'message':json_message
        }
        return self.send_chat_message(content)
    
    commands = {
        'fetch_messages':fetch_messages,
        'new_message':new_message,
        'load_messages':load_messages
    }
    
    def connect(self):
        self.user = self.scope['user']
        self.user2 = self.scope['url_route']['kwargs']['user2']
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        user1 = Profile.objects.get(username = self.user.username)
        user2 = Profile.objects.get(username = self.user2)

        if PrivateChat.objects.filter(
            Q(user1 = user1, user2=user2, guid=self.room_id) | Q(user1=user2, user2=user1, guid=self.room_id)
        ).exists():
            self.room = PrivateChat.objects.filter(
                Q(user1 = user1, user2=user2, guid=self.room_id) | Q(user1=user2, user2=user1, guid=self.room_id)
            )[0]
        else:
            self.room = PrivateChat.objects.create(user1=user1, user2=user2)
        self.room_group_name = 'chat_%s' % str(self.room.guid)
        self.messages_pre_connect_count = self.room.get_messages_count()
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)
          
    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
        
    def send_message(self, message):
        self.send(text_data=json.dumps(message))
        
    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))
        