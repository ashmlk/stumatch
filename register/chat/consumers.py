from asgiref.sync import async_to_sync
import json
from channels.generic.websocket import WebsocketConsumer
from .models import Message, PrivateChat
from main.models import Profile
from django.db.models import Q
from hashids import Hashids

hashid = Hashids(salt='9ejwb NOPHIqwpH9089h 0H9h130xPHJ iojpf909wrwas',min_length=32)

class ChatConsumer(WebsocketConsumer):
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.room = None
        
    def fetch_messages(self, data):
        messages = Message.last_10_messages()
        result = []
        for message in messages:
            json_message =  {
            'id':message.id,
            'author':message.author.username,
            'content':message.content,
            'timestamp':str(message.timestamp),
            'img':message.author.image.url
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
        json_message =  {
            'id':message.id,
            'author':message.author.username,
            'content':message.content,
            'timestamp':str(message.timestamp),
            'img':message.author.image.url
            }
        content = {
            'command':'new_message',
            'message':json_message
        }
        return self.send_chat_message(content)
    
    commands = {
        'fetch_messages':fetch_messages,
        'new_message':new_message
    }
    
    def connect(self):
        self.user = self.scope['user']
        self.user2 = self.scope['url_route']['kwargs']['user2']
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        user1 = Profile.object.get(username = self.user.username)
        user2 = Profile.objects.get(username = self.user2)
        
        self.room_id = hashid.decode(self.room_id)[0]
        
        if PrivateChat.objects.filter(
            Q(user1 = user1, user2=user2, id=self.room_id) | Q(user1=user2, user2=user1, id=self.room_id)
        ).exists():
            self.room = PrivateChat.objects.filter(
                Q(user1 = user1, user2=user2, id=self.room_id) | Q(user1=user2, user2=user1, id=self.room_id)
            )[0]
        else:
            self.room = PrivateChat.objects.create(user1=user1, user2=user2)
        self.room_group_name = 'chat_%s' % str(self.room.get_hashid)
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
        