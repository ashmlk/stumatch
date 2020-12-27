from django.urls import path
from chat import views

app_name = 'chat'

urlpatterns = [
    path('', views.index, name='index'),
    #path('<str:room_name>/', views.room, name='room'),
    path('chat/<str:room_id>/', views.private_chat, name='private-chat'),
    path('send-image/<str:room_id>/', views.create_image, name='send-image-message'),
    path('goc/chat/<str:id>/', views.get_or_create_private_chat, name='get-or-create-private-chat'),
    path('chat/<str:room_id>/message/<str:message_hashed_id>/delete/', views.delete_message, name="delete-chat-message")
]