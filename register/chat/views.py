from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from main.models import Profile
from .models import PrivateChat
from hashids import Hashids

hashid = Hashids(salt='9ejwb NOPHIqwpH9089h 0H9h130xPHJ iojpf909wrwas',min_length=32)
hashids_user = Hashids(salt='wvf935 vnw9py l-itkwnhe 3094',min_length=12)

@login_required
def index(request):
    return render(request, 'chat/index.html')

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
    user2 = Profile.object.get(id = id)
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
    return redirect('chat:private-chat', room_id=chatroom.get_hashid())
    
    
@login_required
def private_chat(request, room_id=None):
    
    if room_id != None:
        return redirect('chat:index')
    try:
        id = hashid.decode(id)[0]
        chatroom = PrivateChat.objects.get(id=id)
    except:
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
    
    context = {
        'room_id': room_id,
        'username':request.user.username,
        'user2':user2
    }
    return render(request, 'chat/room.html', context)