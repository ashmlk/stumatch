from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from .forms import SignUpForm, EditProfileForm, PasswordResetForm
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from hashids import Hashids
from .models import BookmarkBlog, BookmarkBuzz, BookmarkPost, Profile
from home.models import Post, Buzz, Blog
from django.http import JsonResponse
from taggit.models import Tag
from friendship.models import Friend, Follow, Block, FriendshipRequest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

hashids = Hashids(salt='v2ga hoei232q3r prb23lqep weprhza9',min_length=8)

hashids_user = Hashids(salt='wvf935 vnw9py l-itkwnhe 3094',min_length=12)

@login_required
def user_logout(request):
    logout(request)
    return redirect('main:user_login')
    
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            return redirect('main:user_login')
    else:
        form = SignUpForm()
    return render(request, 'main/signup.html', {'form': form})

def user_login(request):
    message = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('home:home')
            else:
                HttpResponse('Account is disabled')
        if user is None:
            message = 'Sorry the username or password you entered is incorrect please try again'
    else:
        message = ''
    return render(request, 'main/user_login.html', {'message': message})

@login_required
def edit_profile(request):
    if request.method=='POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            #return redirect('main:home')
            return redirect(reverse('home:home')) 
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form':form}
        return render(request, 'main/edit_profile.html', args)


@login_required
def add_bookmark(request, hid, obj_type):
    data=dict()
    t=obj_type
    id =  hashids.decode(hid)[0]
    if request.method == 'POST':
        if obj_type=='post':
            model = BookmarkPost
        elif obj_type=='blog':
            model = BookmarkBlog
        elif obj_type=='buzz':
            model = BookmarkBuzz
        user = auth.get_user(request)
        bookmark, created = model.objects.get_or_create(user=user, obj_id=id)
        if not created:
            bookmark.delete()
        context = {
                   'hid':hid,
                   't':t}
        if obj_type!='blog':
            data['html_form'] = render_to_string('main/bookmark/bookmark_dropdown.html',context,request=request)
        else:
            data['html_form'] = render_to_string('main/bookmark/bookmark.html',context,request=request)
    return JsonResponse(data)

@login_required
def bookmarks(request):
    user = request.user
    bookmarked_posts = user.bookmarkpost_set.all()
    bookmarked_blogs = user.bookmarkblog_set.all()
    bookmarked_buzzes = user.bookmarkbuzz_set.all()
    context = {
        'bookmarked_posts':bookmarked_posts,
        'bookmarked_blogs':bookmarked_blogs,
        'bookmarked_buzzes':bookmarked_buzzes,
    }
    return render(request,'main/bookmark/bookmarks_user.html', context)

@login_required
def f_post_tag(request, slug):
    data = dict()
    user = request.user
    tag = get_object_or_404(Tag, slug=slug)
    if request.method == 'POST':
        if user.favorite_post_tags.filter(slug=slug).exists():
            user.favorite_post_tags.remove(tag)
            is_fav = False
        else:
            user.favorite_post_tags.add(tag)
            is_fav = True
        data['html_form'] = render_to_string('main/tags/fav_post.html',{'is_fav':is_fav,'tag':tag},request=request)
        return JsonResponse(data)

@login_required
def f_buzz_tag(request, slug):
    data = dict()
    user = request.user
    tag = get_object_or_404(Tag, slug=slug)
    if request.method == 'POST':
        if user.favorite_buzz_tags.filter(slug=slug).exists():
            user.favorite_buzz_tags.remove(tag)
            is_fav = False
        else:
            user.favorite_buzz_tags.add(tag)
            is_fav = True
        data['html_form'] = render_to_string('main/tags/fav_buzz.html',{'is_fav':is_fav,'tag':tag},request=request)
        return JsonResponse(data)

@login_required
def f_blog_tag(request, slug):
    data = dict()
    user = request.user
    tag = get_object_or_404(Tag, slug=slug)
    if request.method == 'POST':
        if user.favorite_blog_tags.filter(slug=slug).exists():
            user.favorite_post_tags.remove(tag)
            is_fav = False
        else:
            user.favorite_blog_tags.add(tag)
            is_fav = True
        data['html_form'] = render_to_string('main/tags/fav_blog.html',{'is_fav':is_fav,'tag':tag},request=request)
        return JsonResponse(data)


@login_required
def accept_reject_friend_request(request,hid, s):
    data = dict()
    id = hashids_user.decode(hid)[0]
    other_user = get_object_or_404(Profile, id=id)
    user = request.user
    if request.method == 'POST':
        action = int(s)
        is_friend=None
        if action == 0:   
            fr = FriendshipRequest.objects.get(from_user=other_user,to_user=user)
            fr.accept()
            is_friend=True
        elif action == 1:   
            fr = FriendshipRequest.objects.get(from_user=other_user,to_user=user)
            fr.cancel()
        elif action == 3:
            fr = FriendshipRequest.objects.get(from_user=user,to_user=other_user)
            fr.cancel()
            is_friend=False
        data['html_form'] = render_to_string('main/friends/friend_status.html',{'is_friend':is_friend,'user':other_user }, request=request)
        return JsonResponse(data)


@login_required
def add_remove_friend(request, hid, s):
    
    data=dict()
    #remove friend from request.user to the_user
    #user recognized by hid
    id = hashids_user.decode(hid)[0]
    other_user = get_object_or_404(Profile, id=id)
    user = request.user
    if request.method == 'POST':
        pending=None
        is_friend=None
        action = int(s)
        if action == 1:
            #remove friend request from request.user to the_user 
            Friend.objects.remove_friend(user,other_user)
            is_friend = False
        elif action == 0:
            Friend.objects.add_friend(user, other_user)
            pending = True
        data['html_form'] = render_to_string('main/friends/friend_status.html',{'is_friend':is_friend,'pending':pending,'user':other_user} ,request=request)
        return JsonResponse(data)
    

@login_required
def block_user(request, id):
    data=dict()
    id = hashids_user.decode(hid)[0]
    if request.method == "POST":
        wants_to_block = request.user     #request.user submits request to block user
        will_be_blocked = Profile.object.get(id=id) #user to be blocked by request.user
        Block.objects.add_block(wants_to_block, will_be_blocked)
        if Friend.objects.are_friends(wants_to_block, will_be_blocked):
            Friend.objects.remove_friend(wants_to_block, will_be_blocked)
        data['html_form'] = render_to_string('main/friends/friend_status.html',{ 'is_friend':True }, request=request)
        return JsonResponse(data)

@login_required
def friends_main(request):
    
    # dictionaries to keep track of mutual friends between user and 1-param: friends 2-param: friend requests
    mutual_friends_with_friends = dict()
    
    # get friends of request.user
    friends_list = Friend.objects.friends(request.user)
    blocked = Block.objects.blocking(request.user)
    pending_requests = Friend.objects.sent_requests(user=request.user)
    requests = Friend.objects.requests(user=request.user)
    # total friends vs total requests
    total_friends = len(friends_list)
    total_requests = len(requests)
    total_pending = len(Friend.objects.sent_requests(user=request.user))
    total_blocked = len(blocked)
    
    request.session['total_friends'] = total_friends
    request.session['total_requests'] = total_requests
    request.session['total_pending'] = total_pending
    request.session['total_blocked'] = total_blocked
    
    # find number of mutual firneds between user and friends
    for f in friends_list:
        friends_friends = Friend.objects.friends(user=f)
        mutual_friends_with_friends[f.username] = len(set(friends_list) & set(friends_friends))
       
    page = request.GET.get('page', 1)
    paginator = Paginator(friends_list, 10)
    try:
        friends = paginator.page(page)
    except PageNotAnInteger:
        friends = paginator.page(1)
    except EmptyPage:
        friends = paginator.page(paginator.num_pages)
        
   
    context = {
        'friends':friends,
        'friend_requests':friend_requests,
        'mutuals':mutual_friends_with_friends,
        'total_friends':total_friends,
        'total_requests':total_requests,
        'total_pending':total_pending,
        'is_friend':True,
        'friend_active':'active'
    }
    
    return render(request, 'main/friends/friends_friends.html', context)

@login_required
def friend_requests(request):
    
    friends_list = Friend.objects.friends(request.user)
    # param to keep track of ids of users who sent request to request.user
    ids=[]
    mutual_friends_with_requests = dict()
    requests = Friend.objects.requests(user=request.user)
    #append id of users who send friend request to list
    for f in requests:
        ids.append(int(str(f)))  
    # get user objects who sent friend request
    friend_requests_list = Profile.objects.filter(id__in=ids).order_by('last_name')
        # find number ofm utual friends between user an friend requested object @Profile
    for f in friend_requests_list:
        friends_friends = Friend.objects.friends(user=f)
        mutual_friends_with_requests[f.username] = len(set(friends_list) & set(friends_friends))
        
    page = request.GET.get('page', 1)
    paginator = Paginator(friend_requests_list, 10)
    try:
        friend_requests = paginator.page(page)
    except PageNotAnInteger:
        friend_requests = paginator.page(1)
    except EmptyPage:
        friend_requests = paginator.page(paginator.num_pages)
    
    total_friends = request.session.get('total_friends')
    total_requests = request.session.get('total_requests')
    total_pending = request.session.get('total_pending')
       
    context = {
        'friend_requests':friend_requests,
        'mutuals_request':mutual_friends_with_requests,
        'total_friends':total_friends,
        'request_active':'active',
        'total_friends':total_friends,
        'total_requests':total_requests,
        'total_pending':total_pending,
    }
    
    return render(request, 'main/friends/friend_requests.html', context)

@login_required
def friend_pending_requests(request):
    
    
    lister = FriendshipRequest.objects.select_related("from_user", "to_user").filter(from_user=request.user).all()
    
    usernames = [l.to_user.username for l in lister ]
    
    user_list = Profile.objects.filter(username__in=usernames).order_by('last_name')
    total_friends = request.session.get('total_friends')
    total_requests = request.session.get('total_requests')
    total_pending = request.session.get('total_pending')
    
    pending = True
    
    page = request.GET.get('page', 1)
    paginator = Paginator(user_list, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    
    context = {
        'users':users,
        'total_friends':total_friends,
        'pending_active':'active',
        'total_friends':total_friends,
        'total_requests':total_requests,
        'total_pending':total_pending,
        'pending':pending,
    } 

    return render(request, 'main/friends/friends_pending.html', context)

@login_required
def user_same_program(request):
    
    # @param pending - keeps track of users who request.user sent friend request
    # @param requested - keeps track of users who sent friend request to user
    pending = dict()
    requested = dict()
 
    sent =  FriendshipRequest.objects.select_related("from_user", "to_user").filter(from_user=request.user).all()
    requests = Friend.objects.requests(user=request.user)
    #append id of users who send friend request to list
    for f in requests:
        p = Profile.objects.get(id = int(str(f))) 
        requested[p.username] = True
    
    for f in sent:
        pending[f.to_user.username] = True
    
    user = request.user
    uni = user.university
    pro = user.program

    user_list = Profile.objects.same_program(user=user, program=pro, university=uni)
   
    if user_list != None:
        page = request.GET.get('page', 1)
        paginator = Paginator(user_list, 10)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
    elif user_list==None:
        users=None
        
    total_friends = request.session.get('total_friends')
    total_requests = request.session.get('total_requests')
    total_pending = request.session.get('total_pending')
    
    
    context = {
        'users':users,
        'total_friends':total_friends,
        'total_friends':total_friends,
        'total_requests':total_requests,
        'total_pending':total_pending,
        'pending':pending,
        'requested':requested,
        'menu_link_active':'-active',
    } 
    
    return render(request, 'main/friends/friends_same_program.html', context)