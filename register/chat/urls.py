from django.urls import path
from chat import views

app_name = 'chat'

urlpatterns = [
    path('', views.index, name='index'),
    #path('<str:room_name>/', views.room, name='room'),
    path('chat/<str:room_id>/', views.private_chat, name='private-chat'),
    path('goc/chat/<str:id>/', views.get_or_create_private_chat, name='get-or-create-private-chat')
]