from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<user2>\w+)/(?P<room_id>\w+)/$', consumers.ChatConsumer.as_asgi()),
]