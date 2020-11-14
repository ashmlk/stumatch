from asgiref.sync import async_to_sync
import json
from channels.generic.websocket import WebsocketConsumer
from .models import Message
from main.models import Profile

class ChatConsumer(WebsocketConsumer):
        
    def fetch_messages(self, data):
        messages = Message.last_10_messages()
        result = []
        for message in messages:
            json_message =  {
            'author':message.author.username,
            'content':message.content,
            'timestamp':str(message.timestamp)
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
        print(data['message'])
        message = Message.objects.create(
            author=author_user,
            content=data['message'])
        json_message =  {
            'author':message.author.username,
            'content':message.content,
            'timestamp':str(message.timestamp)
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
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

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
        