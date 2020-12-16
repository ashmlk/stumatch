from asgiref.sync import async_to_sync
import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from .models import Message, PrivateChat
from main.models import Profile
from django.db.models import Q
from hashids import Hashids
import math
from channels.db import database_sync_to_async
from .serializers import MessageSerializer

hashid = Hashids(salt='9ejwb NOPHIqwpH9089h 0H9h130xPHJ io9wr',min_length=32)

class ChatConsumer(AsyncWebsocketConsumer):        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.room = None
        self.messages_pre_connect_count = None
        self.last_message = None
        self.page = 1
        self.messages_all_loaded = False
        
    async def fetch_messages(self, data):
        if data['username'] == self.user.username:
            room = await self.get_privatechat_with_id(id=data['room_id'])
            messages, has_messages = await self.get_room_messages()
            self.messages_all_loaded = not has_messages
            result = []
            messages = await self.get_serialized_messages(messages)
            if len(messages) > 0:
                for message in messages:
                    json_message =  {
                        'hashed_id':message['hashed_id'],
                        'author':message['author_username'],
                        'content':message['content'],
                        'timestamp':message['timestamp'],
                        'is_fetching':True,
                    }
                    result.append(json_message)
            content = {
                'command':'messages',
                'messages': result,
                'requested_by':data['username'],
                'is_fetching':True
            }
            if self.messages_all_loaded and len(messages) > 0:
                content['first_message_time'] = await self.get_room_first_message_time()
            await self.send_chat_message(content)
        
    
    async def load_messages(self, data):
        if data['username'] == self.user.username:
            room = await self.get_privatechat_with_id(id=data['room_id'])
            messages, has_messages = await self.get_room_messages(pre_connect_count=self.messages_pre_connect_count, page=self.page+1)
            self.page+=1
            result = []
            messages = await self.get_serialized_messages(messages)
            if not self.messages_all_loaded:
                for message in messages:
                    json_message =  {
                        'hashed_id':message['hashed_id'],
                        'author':message['author_username'],
                        'content':message['content'],
                        'timestamp':message['timestamp'],
                    }
                    result.append(json_message)
            content = {
                'command':'messages',
                'messages': result,
                'requested_by':data['username'],
                'is_loading':True
            }
            self.messages_all_loaded = not has_messages
            if self.messages_all_loaded:
                content['first_message_time'] = await self.get_room_first_message_time()
            await self.send_chat_message(content) 
        
    async def new_message(self, data):
        author = data['from']
        author_user = await self.get_user(username=author)
        message = await self.create_message_object(author=author_user, message=data['message'], room_id=self.room_id)
        message_json = await self.get_serialized_message(message)
        self.last_message = message
        json_message =  {
                'hashed_id':message_json['hashed_id'],
                'author':message_json['author_username'],
                'content':message_json['content'],
                'timestamp':message_json['timestamp'],
                'last_message_content':message_json['content'],
                'last_message_time':message_json['formatted_timestamp']
            }
        
        content = {
            'command':'new_message',
            'message':json_message,
            'is_new_message':True
        }
        # had return statement before
        await self.send_chat_message(content)
    
    # async def typing_start(self, data):
    #     author = data['from']
    #     content = {
    #         'command': 'typing_start',
    #         'from':author,
    #         'is_typing_command':'start'
    #     }

    #     await self.send_chat_message(content)

    # async def typing_stop(self, data):
    #     content = {
    #         'command': 'typing_stop',
    #         'is_typing_command':'stop'
    #     }
    #     await self.send_chat_message(content)
     
    commands = {
        'fetch_messages':fetch_messages,
        'new_message':new_message,
        'load_messages':load_messages,
        # 'typing_start':typing_start,
        # 'typing_stop':typing_stop
    }
    
    '''
    Initiate websocket connection for user to the private chat. If user is authenticated and is part of the private
    chat then connect the user to the private chat
    @param scope['user'] returns the requested user form WebSocket
    @param scope['url_route']['kwargs']['room_id'] returns the requested room based on room_id
    '''
    async def connect(self):
        self.user = self.scope['user']
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        if self.user.is_authenticated:
            chat_exists = await self.check_room_exists()
            if chat_exists:
                self.room, guid = await self.get_privatechat()
                self.room_group_name = 'chat_%s' % str(guid)
                self.messages_pre_connect_count = await self.get_messages_count()
                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )

                await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.commands[data['command']](self, data)
          
    async def send_chat_message(self, message):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
        
    async def send_message(self, message):
        await self.send(text_data=json.dumps(message))
        
    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))
        
        
    @database_sync_to_async
    def check_room_exists(self):
        return PrivateChat.objects.filter(
            Q(user1 = self.user, guid = self.room_id) | Q(user2 = self.user, guid = self.room_id)
        ).exists()
    
    @database_sync_to_async
    def get_privatechat(self):
        pc = PrivateChat.objects.filter(
            Q(user1 = self.user, guid = self.room_id) | Q(user2 = self.user, guid = self.room_id)
        )[0]
        return pc, pc.guid
        
    @database_sync_to_async
    def get_user(self, username):
        return Profile.objects.get(username=username)
    
    @database_sync_to_async
    def get_messages_count(self):
        return self.room.get_messages_count()
    
    @database_sync_to_async
    def get_room_messages(self, pre_connect_count=None, page=None):
        if page == None:
            messages, has_messages =  self.room.get_messages()
            return messages, has_messages
        else:
            messages, has_messages = self.room.get_messages(pre_connect_count=pre_connect_count,page=page)
            return messages, has_messages
    
    @database_sync_to_async
    def get_room_first_message_time(self):
        return self.room.get_first_message_time()
    
    @database_sync_to_async
    def get_privatechat_with_id(self, id):
        return PrivateChat.objects.get(guid=id)
    
    @database_sync_to_async
    def create_message_object(self, author, message, room_id):
        room = PrivateChat.objects.get(guid=room_id)
        message = Message.objects.create(
                author = author,
                content = message,
                privatechat = room
            )
        return message
    
    @database_sync_to_async
    def get_serialized_messages(self, messages):
        return json.loads(json.dumps(MessageSerializer(messages, many=True).data))
    
    @database_sync_to_async
    def get_serialized_message(self, message):
        return json.loads(json.dumps(MessageSerializer(message).data))