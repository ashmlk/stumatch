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
from .models import BookmarkBlog, BookmarkBuzz, BookmarkPost
from home.models import Post, Buzz, Blog
from django.http import JsonResponse
from taggit.models import Tag
from friendship.models import Friend, Follow, Block, FriendshipRequest

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
def friend_request(request, hid):
    
    data=dict()
    #add friend from request.user to other_user
    #user recognized by hid
    id = hashids_user.decode(hid)[0]
    to_user = Profile.object.get(id=id)
    from_user = request.user
    if request.method == 'POST':
        #Default message is always FROM_USER SENT YOU A FRIEND REQUEST
        message = from_user.get_full_name() + " sent you a friend request"
        #create friend request frorm request.user (from_user) to other_user (to_user)
        Friend.objects.add_friend(from_user,to_user,message=message)
        data['html_form'] = render_to_string('main/friends/friend_status.html',request=request)
        return JsonResponse(data)

@login_required
def accept_friend_request(request):
    
    #accept friend request
    pass

@login_required
def reject_friend_request(request):
    
    #reject friend request
    pass

@login_required
def unfriend_user(request, hid):
    
    data=dict()
    #remove friend from request.user to the_user
    #user recognized by hid
    id = hashids_user.decode(hid)[0]
    the_user = Profile.object.get(id=id)
    requested_user = request.user
    if request.method == 'POST':
        #remove friend request from request.user to the_user 
        Friend.objects.remove_friend(requested_user,the_user,message=message)
        data['html_form'] = render_to_string('main/friends/friend_status.html',request=request)
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
        data['html_form'] = render_to_string('main/friends/friend_status.html',request=request)
        return JsonResponse(data)

@login_required
def unblock_user(request, hid):
    
    data=dict()
    id = hashids_user.decode(hid)[0]
    if request.method == "POST":
        wants_to_unblock = request.user     #request.user submits request to unblock user
        will_be_unblocked = Profile.object.get(id=id) #user to be unblocked by request.user
        Block.objects.remove_block(wants_to_ublock, will_be_unlocked)
        data['html_form'] = render_to_string('main/friends/friend_status.html',request=request)
        return JsonResponse(data)




    