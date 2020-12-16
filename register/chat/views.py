from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from main.models import Profile
from .models import PrivateChat, Message
from hashids import Hashids
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect

hashid = Hashids(salt='9ejwb NOPHIqwpH9089h 0H9h130xPHJ io9wr',min_length=32)
hashids_user = Hashids(salt='wvf935 vnw9py l-itkwnhe 3094',min_length=12)
hashid_messages = Hashids(salt='18BIOHBubi 23Ubliilb 89sevsdfuv wuboONEO3489',min_length=32)

@login_required
def index(request):
    
    users, last_message_content = PrivateChat.objects.get_user_chats(user=request.user)
    context = {
        'users':users,
        'last_message_content':last_message_content
    }
    return render(request, 'chat/index.html', context)

# @login_required
# def room(request, room_name):
#     return render(request, 'chat/room.html', {
#         'room_name': room_name,
#         'username':request.user.username
#     })
    
@login_required
def get_or_create_private_chat(request, id):
    
    id = hashids_user.decode(id)[0]
    user1 = request.user
    user2 = Profile.objects.get(id = id)
    try:
        if PrivateChat.objects.filter(user1=user1, user2=user2):
            chatroom = PrivateChat.objects.get(user1=user1, user2=user2)
        elif PrivateChat.objects.filter(user1=user2, user2=user1):
            chatroom = PrivateChat.objects.get(user1=user2, user2=user1)
        else:
            chatroom = PrivateChat.objects.create(user1=user1, user2=user2)
    except Exception as e:
        print(e)
        return redirect('chat:index')
    print(chatroom.guid)
    return redirect(reverse('chat:private-chat', kwargs={'room_id':chatroom.guid}))
    

@login_required
def private_chat(request, room_id):
    
    #try:
    chatroom = PrivateChat.objects.get(guid=room_id)
    # except Exception as e:
    #     print(e)
    #     return redirect('chat:index')
    if not request.user in [chatroom.user1, chatroom.user2]:
        return redirect('chat:index')
    user2 = chatroom.user2 if chatroom.user1 == request.user else chatroom.user1     
    messages_all = chatroom.messages.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(messages_all, 10)
    try:
        messages = paginator.page(page)
    except PageNotAnInteger:
        messages = paginator.page(1)
    except EmptyPage:
        messages = paginator.page(paginator.num_pages)
    
    users, last_message_content = PrivateChat.objects.get_user_chats(user=request.user)
    
    context = {
        'room_id': room_id,
        'username':request.user.username,
        'user2':user2,
        'users':users,
        'last_message_content':last_message_content
    }
    return render(request, 'chat/room.html', context)

@login_required
def delete_message(request, room_id, message_hashed_id):
    data = dict()
    if request.user.is_authenticated:
        message = get_object_or_404(Message, id=hashid_messages.decode(message_hashed_id)[0])
        room = get_object_or_404(PrivateChat, guid=room_id)
        if message.privatechat == room and message.author == request.user:
            message.delete()
            data['success'] = True
            return JsonResponse(data)