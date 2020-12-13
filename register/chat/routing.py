from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'chat/(?P<room_id>\w+)/$', consumers.ChatConsumer.as_asgi()),
    #re_path(r'chat/', consumers.ChatConsumer.as_asgi()),
]