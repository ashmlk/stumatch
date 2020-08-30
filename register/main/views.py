from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.shortcuts import render, redirect
from .forms import SignUpForm, EditProfileForm, PasswordResetForm, ConfirmPasswordForm
from django.views.generic.edit import UpdateView
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
from datetime import datetime, timezone
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from main.decorators import confirm_password

hashids = Hashids(salt='v2ga hoei232q3r prb23lqep weprhza9',min_length=8)

hashids_user = Hashids(salt='wvf935 vnw9py l-itkwnhe 3094',min_length=12)

class ConfirmPasswordView(UpdateView):
    
    form_class = ConfirmPasswordForm
    template_name = 'main/settings/confirm_password.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return self.request.get_full_path()  

def policy_html(request):
    
    return render(request, 'web_docs/policy/index.html')

@login_required
def get_notifications(request):
    
    notifications_unread = request.user.notifications.unread()
    notifications_read = request.user.notifications.read()
    read_count = notifications_read.count()
    
    context = {
        'notifications_read':notifications_read,
        'notifications_unread':notifications_unread,
        'read_count':read_count
        }
    
    return render(request, 'main/notifications/notifications_list.html', context)


@login_required
def delete_notification(request):
    data = dict()
    """marking notification(s) as read"""
    notice_id = request.GET.get("notice_id", None)
    if notice_id: # if notice_id exists means one notification is being updated
        request.user.notifications.get(id=notice_id).delete()
        data['single_notification_delete'] = True
        return JsonResponse(data)
    else: # if notice_id does not exists we are marking all user notifications as read
        request.user.notifications.all().delete()
        return redirect('main:get-notifications')

@login_required
def mark_notification_as_read(request):
    
    data = dict()
    """marking notification(s) as read"""
    notice_id = request.GET.get("notice_id", None)
    if notice_id: # if notice_id exists means one notification is being updated
        request.user.notifications.get(id=notice_id).mark_as_read()
        data['single_notification_marked'] = True
        return JsonResponse(data)
    else: # if notice_id does not exists we are marking all user notifications as read
        request.user.notifications.mark_all_as_read()
        return redirect('main:get-notifications')
    
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
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated.')
            return redirect('main:change-password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'main/settings/change_password.html', {
        'form': form,
        'privacy_active':'setting-link-active',
    })
    
@login_required
def edit_profile(request):
    
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            #return redirect('main:home')
            return redirect(reverse('main:settings-edit')) 
    else:
        form = EditProfileForm(instance=request.user)
        if request.user.image.url != '/media/defaults/user/default_u_i.png':
            image_not_default = True
        else:
            image_not_default = False
        context = {
            'form':form,
            'image_not_default':image_not_default,
            'account_active':'setting-link-active'
            }
        print(request.user.image.url)
        return render(request, 'main/settings/edit_profile.html', context)

@login_required
def update_image(request, hid):
    
    data = dict()
    id = hashids_user.decode(hid)[0]
    user = Profile.objects.get(id=id)
    if request.method == "POST":
        image_not_default = True
        if request.user == user:
            user = request.user
            if request.user.is_authenticated:
                print(request.FILES)
                image = request.FILES['image']
                user.image = image
                user.save()
        if request.user.image.url == '/media/defaults/user/default_u_i.png':
            image_not_default = False  
        context = {
            'image_not_default':image_not_default
        } 
        data['image_updated'] = render_to_string('main/settings/image_update.html',context,request=request)
        return JsonResponse(data)

@login_required
def remove_image(request, hid):
    image_not_default = True
    data = dict()
    id = hashids_user.decode(hid)[0]
    user = Profile.objects.get(id=id)
    if request.method == "POST":
        if request.user == user:
            if user.image != '/media/defaults/user/default_u_i.png':
                user.set_image_to_default()
                image_not_default = False 
        context = {
            'image_not_default':image_not_default
        }        
        data['image_updated'] = render_to_string('main/settings/image_update.html',context,request=request)   
    else:
        if request.user == user:
            if request.user.is_authenticated: 
                context = {
                    'user':request.user,
                }   
                data['html_form'] = render_to_string('main/settings/image_delete_confirm.html',context,request=request)   
    return JsonResponse(data)    

@login_required
def privacy_security(request):
    
    if request.user.is_authenticated:
        user = request.user
        context = {
            'user':user,
            'privacy_active':'setting-link-active',

        }
        return render(request, 'main/settings/privacy_security_menu.html', context)

@login_required
def set_public_private(request):
    
    data = dict()
    
    if request.method == "POST":
        hid = request.POST.get('hid', None)
        id = hashids_user.decode(hid)[0]
        user = Profile.objects.get(id=id)
        if user == request.user:
            
            choice = request.POST.get('publicprivate-input-check', None)
            if choice == "pupstvbevo":
                if user.public == False:
                    user.public = True
                    disable_ranking = ''
                    user.save()
            elif choice == "prpstvbfo":
                if user.public == True:
                    user.public = False
                    disable_ranking = 'disabled'
                    user.save()
    
            if choice != None:
                if user.rank_objects == True:
                    ranking_on = 'checked'
                    ranking_off = ''
                elif user.rank_objects == False:
                    ranking_off = 'checked'  
                    ranking_on = ''
                context = {
                    'ranking_on':ranking_on,
                    'ranking_off':ranking_off,
                    'disable_ranking': disable_ranking
                }
                data['update_ranking'] = True
                data['ranking_form'] = render_to_string('main/settings/ranking_form.html',context,request=request)
                
            else:
                choice_r = request.POST.get('ranking-input-check', None)
                if choice_r == 'rfuon':
                    user.rank_objects = True
                    user.save()
                elif choice_r == 'rfuoff':
                    user.rank_objects = False
                    user.save()
                data['complete'] = 'completed'
            return JsonResponse(data)
            
    else:
        if request.user.is_authenticated:
            disable_ranking = ''
            user = request.user
            if user.public == True:
                public_check = 'checked'
                private_check = ''
            elif user.public == False:
                private_check = 'checked'
                disable_ranking = 'disabled'
                public_check = '' 
            if user.rank_objects == True:
                ranking_on = 'checked'
                ranking_off = ''
            elif user.rank_objects == False:
                ranking_off = 'checked'  
                ranking_on = ''
            context = {
                'public_check':public_check,
                'private_check':private_check,
                'privacy_active':'setting-link-active',
                'ranking_on':ranking_on,
                'ranking_off':ranking_off,
                'disable_ranking': disable_ranking
            }
            return render(request,'main/settings/public_private.html', context)

        
@login_required
def search_settings(request):
    
    data = dict()
    
    searches = request.user.recent_searches.order_by('-time_stamp')
    
    if request.method == 'POST':
        
        if request.user.is_authenticated:
            choice = request.POST.get('onoffinput-check', None)
            if choice == "searchoff":
                if request.user.save_searches == True:
                    request.user.save_searches = False
                    if request.user.recent_searches:
                        request.user.recent_searches.clear()
                    request.user.save()
                    data['update_search_settings'] = True
            elif choice == "searchon":
                if request.user.save_searches == False:
                    request.user.save_searches = True
                    request.user.save()
                    data['update_search_settings'] = True
            
            data['search_settings_form'] = render_to_string('main/settings/search_settings_input.html',request=request)
            return JsonResponse(data)
    
    else:
        
        context = {
            'searches':searches,
            'privacy_active':'setting-link-active',
        }         

        return render(request, 'main/settings/search_settings_main.html', context)

@login_required
def notification_settings_all(request):
    
    data = dict()
    
    if request.method == 'POST':
        
        if request.user.is_authenticated:
                choice = request.POST.get('onoffinput-check', None)
                if choice == "notifyoff":
                    if request.user.get_notify  == True:
                        request.user.get_notify  = False
                        request.user.save()
                        data['update_notifications_settings'] = True
                elif choice == "notifyon":
                    if request.user.get_notify == False:
                        request.user.get_notify = True
                        request.user.save()
                        data['update_notifcaions_settings'] = True
                
                data['notifications_form'] = render_to_string('main/settings/notifications/notifications_pause_all.html',request=request)
                return JsonResponse(data)
            
    else:
        context = {
            'notifcation_active':'setting-link-active',
        }
        return render(request, 'main/settings/notifications/notifications_all.html', context)
    
@login_required
def notifications_post_all(request):
    
    data = dict()
    
    if request.user.is_authenticated:
        choice = request.POST.get('onoffinput-check', None)
        if choice == "postalloff":
            if request.user.get_post_notify_all == True:
                request.user.get_post_notify_all = False
                request.user.save()
            data['notifications_form'] = render_to_string('main/settings/notifications/notifications_post_all.html',request=request)
            return JsonResponse(data)
            
        if choice == "postallon":
            if request.user.get_post_notify_all == False:
                request.user.get_post_notify_all = True
                request.user.save()
                data['notifications_form'] = render_to_string('main/settings/notifications/notifications_post_all.html',request=request)
                return JsonResponse(data)
                
        if choice == "postcommentson":
            if request.user.get_post_notify_comments == False:
                request.user.get_post_notify_comments = True
                request.user.save()
            data['notifications_form'] = render_to_string('main/settings/notifications/notifications_post_comments.html',request=request)
            return JsonResponse(data)
          
        if choice == "postcommentsoff":
            if request.user.get_post_notify_comments == True:
                request.user.get_post_notify_comments = False
                request.user.save()
            data['notifications_form'] = render_to_string('main/settings/notifications/notifications_post_comments.html',request=request)
            return JsonResponse(data)
                         
        if choice == "postlikeson":
            if request.user.get_post_notify_likes == False:
                request.user.get_post_notify_likes = True
                request.user.save()
            data['notifications_form'] = render_to_string('main/settings/notifications/notifications_post_likes.html',request=request)
            return JsonResponse(data)
                          
        if choice == "postlikesoff":
            if request.user.get_post_notify_likes == True:
                request.user.get_post_notify_likes = False
                request.user.save()
            data['notifications_form'] = render_to_string('main/settings/notifications/notifications_post_likes.html',request=request)
            return JsonResponse(data)
    context = {
        'notifcation_active':'setting-link-active',
    }
    return render(request, 'main/settings/notifications/notifications_post.html', context)

@login_required
def notifications_buzz_all(request):
    
    data = dict()
    
    if request.user.is_authenticated:
        choice = request.POST.get('onoffinput-check', None)
        if choice == "buzzalloff":
            if request.user.get_buzz_notify_all == True:
                request.user.get_buzz_notify_all = False
                request.user.save()
            data['notifications_form'] = render_to_string('main/settings/notifications/notifications_buzz_all.html',request=request)
            return JsonResponse(data)
        if choice == "buzzallon":
            if request.user.get_buzz_notify_all == False:
                request.user.get_buzz_notify_all = True
                request.user.save()
                data['notifications_form'] = render_to_string('main/settings/notifications/notifications_buzz_all.html',request=request)
            return JsonResponse(data)    
        
        if choice == "buzzcommentson":
            if request.user.get_buzz_notify_comments == False:
                request.user.get_buzz_notify_comments = True
                request.user.save()
            data['notifications_form'] = render_to_string('main/settings/notifications/notifications_buzz_comments.html',request=request)
            return JsonResponse(data)   
        
        if choice == "buzzcommentsoff":
            if request.user.get_buzz_notify_comments == True:
                request.user.get_buzz_notify_comments = False
                request.user.save()
            data['notifications_form'] = render_to_string('main/settings/notifications/notifications_buzz_comments.html',request=request)
            return JsonResponse(data)   
        
        if choice == "buzzlikeson":
            if request.user.get_buzz_notify_likes == False:
                request.user.get_buzz_notify_likes = True
                request.user.save()
            data['notifications_form'] = render_to_string('main/settings/notifications/notifications_buzz_likes.html',request=request)
            return JsonResponse(data)   
         
        if choice == "buzzlikesoff":
            if request.user.get_buzz_notify_likes == True:
                request.user.get_buzz_notify_likes = False
                request.user.save()
            data['notifications_form'] = render_to_string('main/settings/notifications/notifications_buzz_likes.html',request=request)
            return JsonResponse(data)
        
    context = {
            'notifcation_active':'setting-link-active',
        }
    return render(request, 'main/settings/notifications/notifications_buzz.html', context)

@login_required
def notifications_blog_all(request):
    
    data = dict()
    
    if request.user.is_authenticated:
        choice = request.POST.get('onoffinput-check', None)
        if choice == "blogalloff":
            if request.user.get_blog_notify_all == True:
                request.user.get_blog_notify_all = False
                request.user.save()
            data['notifications_form'] = render_to_string('main/settings/notifications/notifications_blog_all.html',request=request)
            return JsonResponse(data)
        
        if choice == "blogallon":
            if request.user.get_blog_notify_all == False:
                request.user.get_blog_notify_all = True
                request.user.save()
                data['notifications_form'] = render_to_string('main/settings/notifications/notifications_blog_all.html',request=request)
            return JsonResponse(data)    
        
        if choice == "blogcommentson":
            if request.user.get_blog_notify_comments == False:
                request.user.get_blog_notify_comments = True
                request.user.save()
            data['notifications_form'] = render_to_string('main/settings/notifications/notifications_blog_comments.html',request=request)
            return JsonResponse(data)  
        
        if choice == "blogcommentsoff":
            if request.user.get_blog_notify_comments == True:
                request.user.get_blog_notify_comments = False
                request.user.save()
            data['notifications_form'] = render_to_string('main/settings/notifications/notifications_blog_comments.html',request=request)
            return JsonResponse(data)   
        
        if choice == "bloglikeson":
            if request.user.get_blog_notify_likes == False:
                request.user.get_blog_notify_likes = True
                request.user.save()
            data['notifications_form'] = render_to_string('main/settings/notifications/notifications_blog_comments.html',request=request)
            return JsonResponse(data)
        
        if choice == "bloglikesoff":
            if request.user.get_blog_notify_likes == True:
                request.user.get_blog_notify_likes = False
                request.user.save()
            data['notifications_form'] = render_to_string('main/settings/notifications/notifications_blog_comments.html',request=request)
            return JsonResponse(data)
    context = {
        'notifcation_active':'setting-link-active',
    }
    return render(request, 'main/settings/notifications/notifications_blog.html', context)        

@login_required
def notifications_friends_all(request):
    
    data = dict()
    
    if request.user.is_authenticated:
        choice = request.POST.get('onoffinput-check', None)
        if choice == "friendrequestoff":
            if request.user.get_friendrequest_notify == True:
                request.user.get_friendrequest_notify = False
                request.user.save()
            data['notifications_form'] = render_to_string('main/settings/notifications/notifications_friends_all.html',request=request)
            return JsonResponse(data)
        
        if choice == "friendrequeston":
            if request.user.get_friendrequest_notify == False:
                request.user.get_friendrequest_notify = True
                request.user.save()
                data['notifications_form'] = render_to_string('main/settings/notifications/notifications_friends_all.html',request=request)
            return JsonResponse(data)    
        
        if choice == "friendrequestacceptedon":
            if request.user.get_friendrequestaccepted_notify == False:
                request.user.get_friendrequestaccepted_notify = True
                request.user.save()
            data['notifications_form'] = render_to_string('main/settings/notifications/notifications_blog_comments.html',request=request)
            return JsonResponse(data)  
        
        if choice == "friendrequestacceptedoff":
            if request.user.get_friendrequestaccepted_notify == True:
                request.user.get_friendrequestaccepted_notify = False
                request.user.save()
            data['notifications_form'] = render_to_string('main/settings/notifications/notifications_blog_comments.html',request=request)
            return JsonResponse(data)   
        
    context = {
        'notifcation_active':'setting-link-active',
    }
    return render(request, 'main/settings/notifications/notifications_friends.html', context)     
        
@login_required
def get_blocking(request):
    
    if request.user.is_authenticated:
        blocked = Block.objects.blocking(request.user)
        is_blocked = True
        context = {
            'users':blocked,
            'is_blocked':is_blocked,
            'blocked_active':'setting-link-active',
        }
        return render(request,'main/settings/blocked_users.html', context)
    
@login_required
def login_info(request):
    
    if request.user.is_authenticated:
        last_login_utc = Profile.objects.get(username=request.user.username).last_login
        last_login = last_login_utc.replace(tzinfo=timezone.utc).astimezone(tz=None)
        date_joined_utc = Profile.objects.get(username=request.user.username).date_joined
        date_joined = date_joined_utc.replace(tzinfo=timezone.utc).astimezone(tz=None)
        
        context = {
            'last_login':last_login,
            'date_joined':date_joined,
            'privacy_active':'setting-link-active',
        }
        
        return render(request,'main/settings/login_info.html', context)
        
@login_required
def deletion_menu(request):
    
    if request.user.is_authenticated:
        return render(request, 'main/settings/deletion/menu.html',{'privacy_active':'setting-link-active'})
    else:
        return redirect('main:settings-edit')
    
@login_required
@confirm_password
def deletion_post(request):
    
    if request.user.is_authenticated:
        obj = request.GET.get('t', None)
        msg_dict = {
                    'all':'Are you sure you want to delete all your posts permanently?',
                    'comments':'Are you sure you want to delete all your comments permanently?',
                    'likes':'Are you sure you want to remove all your likes permanently?'
        }
        
        title_dict = {
                    'all':'Delete all your posts',
                    'comments':'Delete all your comments',
                    'likes':'Remove all your likes'
        }
        
        message = msg_dict[obj]
        title = title_dict[obj]
        
        if request.method == 'POST':
            
            if obj == 'all':
                if request.user.posts.exists():
                    request.user.posts.all().delete()
                success_message = "Deleted all your posts successfully"
                
            elif obj == 'comments':
                if request.user.comment_set.exists():
                    request.user.comment_set.all().delete()
                success_message = "Deleted all your comments successfully"
            
            elif obj == 'likes':
                if request.user.post_likes.exists():
                    request.user.post_likes.all().clear()
                success_message = "Removed all your likes successfully"
                
            messages.success(request,success_message)
            return redirect('main:delete-menu')
        
        context = {
            'message':message,
            'obj':obj,
            'title':title,
            'privacy_active':'setting-link-active',
        }
        
        return render(request, 'main/settings/deletion/post.html', context)
    
    else:
        error_message = "There was an issue processing your request"
        messages.error(request,error_message)
        return redirect('main:delete-menu')
        
@login_required
@confirm_password
def deletion_buzz(request):
    
    if request.user.is_authenticated:
        obj = request.GET.get('t', None)
        msg_dict = {
                    'all':'Are you sure you want to delete all your buzzes permanently?',
                    'replies':'Are you sure you want to delete all your replies permanently?',
                    'likes':'Are you sure you want to remove all your likes, dislikes, and wots permanently?'
        }
        
        title_dict = {
                    'all':'Delete all your buzzes',
                    'replies':'Delete all your replies',
                    'likes':'Remove all your likes, dislikes, and wots'
        }
        
        message = msg_dict[obj]
        title = title_dict[obj]
        
        if request.method == 'POST':
            
            if obj == 'all':
                if request.user.buzz_set.exists():
                    request.user.buzz_set.all().delete()
                success_message = "Deleted all your buzzes successfully"
                
            elif obj == 'replies':
                if request.user.buzzreply_set.exists():
                    request.user.buzzreply_set.all().delete()
                success_message = "Deleted all your replies successfully"
            
            elif obj == 'likes':
                if request.user.likes.exists():
                    request.user.likes.clear()
                if request.user.dislikes.exists():
                    request.user.dislikes.clear()
                if request.user.wots.exists():
                    request.user.wots.clear()
                success_message = "Removed all your likes, dislikes and wots successfully"
            
            messages.success(request,success_message)
            return redirect('main:delete-menu')
        
        context = {
            'message':message,
            'obj':obj,
            'title':title,
            'privacy_active':'setting-link-active',
        }
        
        return render(request, 'main/settings/deletion/buzz.html', context)
    
    else:
        error_message = "There was an issue processing your request"
        messages.error(request,error_message)
        return redirect('main:delete-menu')
    
@login_required
@confirm_password
def deletion_blog(request):
    
    if request.user.is_authenticated:
        obj = request.GET.get('t', None)
        msg_dict = {
                    'all':'Are you sure you want to delete all your blogs permanently?',
                    'replies':'Are you sure you want to delete all your blog replies permanently?',
                    'likes':'Are you sure you want to remove all your blog likes permanently?'
        }
        
        title_dict = {
                    'all':'Delete all your blogs',
                    'replies':'Delete all your blog replies',
                    'likes':'Remove all your likes'
        }
        
        message = msg_dict[obj]
        title = title_dict[obj]
        
        if request.method == 'POST':
            
            if obj == 'all':
                if request.user.blog_set.exists():
                    request.user.blog_set.all().delete()
                success_message = "Deleted all your blogs successfully"
                
            elif obj == 'replies':
                if request.user.blogreply_set.exists():
                    request.user.blogreply_set.all().delete()
                success_message = "Deleted all your blog replies successfully"
            
            elif obj == 'likes':
                if request.user.blog_likes.exists():
                    request.user.blog_likes.all().clear()
                success_message = "Removed all your blog likes successfully"
            
            messages.success(request,success_message)
            return redirect('main:delete-menu')
        
        context = {
            'message':message,
            'obj':obj,
            'title':title,
            'privacy_active':'setting-link-active',
        }
        
        return render(request, 'main/settings/deletion/blog.html', context)

    else:
        error_message = "There was an issue processing your request"
        messages.error(request,error_message)
        return redirect('main:delete-menu')
    
@login_required
@confirm_password
def deletion_course(request):
    
    if request.user.is_authenticated:
        obj = request.GET.get('t', None)
        msg_dict = {
                    'all':'Are you sure you want to remove all your courses permanently?',
                    'reviews':'Are you sure you want to delete all your course reviews permanently?',
        }
        
        title_dict = {
                    'all':'Delete all your courses',
                    'reviews':'Delete all your course reviews',
        }
        
        message = msg_dict[obj]
        title = title_dict[obj]
        
        if request.method == 'POST':
            
            if obj == 'all':
                if request.user.courses.exists():
                    request.user.courses.clear()
                success_message = "Removed all your courses successfully"
                
            elif obj == 'reviews':
                if request.user.review_set.exists():
                    request.user.review_set.all().delete()
                success_message = "Deleted all your course reviews successfully"
            
            
            messages.success(request,success_message)
            return redirect('main:delete-menu')
        
        context = {
            'message':message,
            'obj':obj,
            'title':title,
            'privacy_active':'setting-link-active',
        }
        
        return render(request, 'main/settings/deletion/course.html', context)

    else:
        error_message = "There was an issue processing your request"
        messages.error(request,error_message)
        return redirect('main:delete-menu')
    
    
@login_required
@confirm_password
def deletion_account(request):
    
    if request.user.is_authenticated:  
        if request.method == 'POST':
   
            form = ConfirmPasswordForm(request.POST, instance=request.user)
            if form.is_valid():
                #request.user.delete()
                print("lol")
                success_message = "Your account has been removed"
                messages.success(request,success_message)
                return redirect('main:delete-menu')

            else:
                error_message = "There was an issue processing your request, please try again"
                messages.error(request,error_message)
                return redirect('main:account-deletion')

        form = ConfirmPasswordForm(instance=request.user)        
        return render(request, 'main/settings/deletion/account.html', {'form':form,'privacy_active':'setting-link-active'})
        
    else:
        error_message = "There was an issue processing your request"
        messages.error(request,error_message)
        return redirect('main:delete-menu')
           
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
            user.favorite_blog_tags.remove(tag)
            is_fav = False
            print("oh no")
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
            if other_user.get_friendrequestaccepted_notify:
                message = "CON_FRRE" + "has accepted your friend request"
                notify.send(sender=user, recipient=other_user, verb=message, target=fr)
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
            Friend.objects.remove_friend(user, other_user)
            is_friend = False
        elif action == 0:
            Friend.objects.add_friend(user, other_user) # send a friend request to other_user
            pending = True
            if other_user.get_friendrequest_notify:
                fr = FriendshipRequest.objects.get(from_user=user,to_user=other_user)
                message = "CON_FRRE" + "has sent you a friend request"
                notify.send(sender=user, recipient=other_user, verb=message, target=fr)
        data['html_form'] = render_to_string('main/friends/friend_status.html',{'is_friend':is_friend,'pending':pending,'user':other_user} ,request=request)
        return JsonResponse(data)
    

@login_required
def block_user(request, hid):
    
    data=dict()
    id = hashids_user.decode(hid)[0]
    wants_to_block = request.user     #request.user submits request to block user
    will_be_blocked = Profile.objects.get(id=id) #user to be blocked by request.user
    if request.method == "POST":
        Block.objects.add_block(wants_to_block, will_be_blocked)
        """ After blocking a user update the session holding the blockers_id """
        blockers_list = Block.objects.blocked(request.user)
        request.session['blockers'] = [u.id for u in blockers_list]
        if Friend.objects.are_friends(wants_to_block, will_be_blocked):
            Friend.objects.remove_friend(wants_to_block, will_be_blocked)
        if FriendshipRequest.objects.filter(from_user=will_be_blocked,to_user=wants_to_block).exists():
            fr = FriendshipRequest.objects.get(from_user=will_be_blocked,to_user=wants_to_block)
            fr.delete()
        elif FriendshipRequest.objects.filter(from_user=wants_to_block,to_user=will_be_blocked).exists():
            fr = FriendshipRequest.objects.get(from_user=wants_to_block,to_user=will_be_blocked)
            fr.delete()
        return redirect('main:get_user',username=will_be_blocked.username)
    else:
        data['html_form'] = render_to_string('main/userhome/block_user_form.html',\
            {'wants_to_block':wants_to_block,'will_be_blocked':will_be_blocked} ,request=request)  
    return JsonResponse(data)

@login_required
def unblock_user(request, hid):
    
    id = hashids_user.decode(hid)[0]
    wants_to_unblock = request.user     #request.user submits request to unblock user
    will_be_unblock = Profile.objects.get(id=id) #user to be unblocked by request.user (SIGNED IN USER)
    """ After blocking a user update the session holding the blockers_id """
    blockers_list = Block.objects.blocked(request.user)
    request.session['blockers'] = [u.id for u in blockers_list]
    if request.method=="POST":
        if Block.objects.is_blocked(wants_to_unblock, will_be_unblock):
            Block.objects.remove_block(wants_to_unblock,will_be_unblock)
            return redirect('main:get_user',username=will_be_unblock.username)
        

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
        # find number ofm mutual friends between user an friend requested object @Profile
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
    users = user_list = None
    needs_edit = False
    
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

    if uni and program:
        user_list = Profile.objects.same_program(user=user, program=pro, university=uni)
    else:
        needs_edit = True
        
    if user_list != None:
        page = request.GET.get('page', 1)
        paginator = Paginator(user_list, 10)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        
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
        'needs_edit':needs_edit,
        'menu_link_active':'-active',
    } 
    
    return render(request, 'main/friends/friends_same_program.html', context)

@login_required
def user_tags(request,username=None):

    s = 'Tags'
    username = request.user.get_username()
    
    o = request.GET.get('o','post')
    
    num_obj = request.user.favorite_post_tags.count() + request.user.favorite_buzz_tags.count() + request.user.favorite_blog_tags.count()
    if num_obj < 1:
        s= "Tag"
    if o == 'post':
        tags = request.user.favorite_post_tags.all()
    elif o == 'buzz':
        tags = request.user.favorite_buzz_tags.all()
    elif o == 'blog':
        tags = request.user.favorite_blog_tags.all()

    context = {
            'tags':tags,
            o+'_active':'-active',
            'is_'+o:True,
            's':s,
            'num_obj':num_obj
         }
    
    return render(request, 'main/tags/user_tags.html', context)

@login_required
def get_user(request,username):
    
    user = get_object_or_404(Profile, username=username)
      
    if request.user==user:
        pnum = user.post_set.count()
        bznum = user.buzz_set.count()
        blnum = user.blog_set.count()
        cnum = user.courses.count()
        courses = user.courses.distinct('course_code','course_instructor')[:4]
        posts = user.post_set.order_by('last_edited')[:4]
        blogs = user.blog_set.order_by('last_edited')[:4]
        friends = Friend.objects.friends(user)
        num_friends = len(friends)
        context = {
            'user':user,
            'pnum':pnum,
            'blnum':blnum,
            'bznum':bznum,
            'cnum':cnum,
            'courses':courses,
            'pro_active':'-active',
            'friends':friends[:6],
            'num_friends':num_friends,
            'posts':posts,
            'blogs':blogs
        }
        return render(request, 'main/userhome/request_user.html', context)
    
    elif Friend.objects.are_friends(request.user, user):
        
        mutual_courses = \
            user.courses.values('course_code','course_instructor','course_university','course_university_slug','course_instructor_slug') & \
                request.user.courses.values('course_code','course_instructor','course_university','course_university_slug','course_instructor_slug')
        

        pnum = user.post_set.count()
        blnum = user.blog_set.count()
        cnum = user.courses.count()
        
        friends = Friend.objects.friends(user)[:6]
        num_friends = len(friends)

        post_list = user.post_set.order_by('last_edited')
        page = request.GET.get('page_posts', 1)
        paginator = Paginator(post_list, 4)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        
        blog_list = user.blog_set.order_by('last_edited')
        page = request.GET.get('page_blogs', 1)
        paginator = Paginator(blog_list, 4)
        try:
            blogs = paginator.page(page)
        except PageNotAnInteger:
            blogs = paginator.page(1)
        except EmptyPage:
            blogs = paginator.page(paginator.num_pages)
        
        context = {
            'user':user,
            'is_friend':True,
            'pnum':pnum,
            'blnum':blnum,
            'cnum':cnum,
            'posts':posts, 
            'blogs':blogs,
            'friends':friends,
            'num_friends':num_friends,'pro_active':'-active',
            'courses':mutual_courses
        }
        
        return render(request, 'main/userhome/view_profile.html', context)
    
    elif Block.objects.is_blocked(request.user, user):
        context = {
            'user':user,
        }
        return render(request, 'main/userhome/blocked_user.html', context)
    
    elif Block.objects.is_blocked(user, request.user):
        context = {
            'message':'User not found.'
        }
        return render(request, 'main/userhome/request_blocked.html', context)
    
    # if use is private just do not show anything
    elif user.public==False:
        sent_request=False
        pending=False
        if FriendshipRequest.objects.filter(from_user=user,to_user=request.user).exists():
            status_message = user.get_full_name() + " has sent you a friend request."
            sent_request=True
        elif FriendshipRequest.objects.filter(from_user=request.user,to_user=user).exists():
            status_message = "Your friend request is pending."
            pending=True
        else:
            status_message = "Do you know " + user.get_full_name() + "?"
        context = {
            'user':user,
            'sent_request':sent_request,
            'pending':pending,
            'status_message':status_message
        }
        return render(request, 'main/userhome/private_user.html', context)
    
    # if use page is public it will be same as friend except the add button, pending status of friend
    elif user.public==True and not Friend.objects.are_friends(request.user, user):
        
        requested=pending=addfriend=False
        
        if FriendshipRequest.objects.filter(from_user=user,to_user=request.user).exists():
            requested=True   
        elif FriendshipRequest.objects.filter(from_user=request.user,to_user=user).exists():
            pending=True
        else:
            addfriend=True  

        mutual_courses = \
            user.courses.values('course_code','course_instructor','course_university','course_university_slug','course_instructor_slug') & \
                request.user.courses.values('course_code','course_instructor','course_university','course_university_slug','course_instructor_slug')
        
        pnum = user.post_set.count()
        blnum = user.blog_set.count()
        cnum = user.courses.count()
        
        friends = Friend.objects.friends(user)[:6]
        num_friends = len(friends)

        post_list = user.post_set.order_by('last_edited')
        page = request.GET.get('page_posts', 1)
        paginator = Paginator(post_list, 4)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        
        blog_list = user.blog_set.order_by('last_edited')
        page = request.GET.get('page_blogs', 1)
        paginator = Paginator(blog_list, 4)
        try:
            blogs = paginator.page(page)
        except PageNotAnInteger:
            blogs = paginator.page(1)
        except EmptyPage:
            blogs = paginator.page(paginator.num_pages)
        
        context = {
            'user':user,
            'pnum':pnum,
            'blnum':blnum,
            'cnum':cnum,
            'posts':posts, 
            'blogs':blogs,
            'friends':friends,
            'requested':requested,
            'addfriend':addfriend,
            'pending':pending,
            'num_friends':num_friends,'pro_active':'-active',
            'courses':mutual_courses
        }
        
        return render(request, 'main/userhome/view_profile.html', context)

@login_required   
def get_user_friends(request):
    
    is_friend = requested = pending = addfriend = False
    
    hid = request.GET.get('id', None)
    id = hashids_user.decode(hid)[0]
    
    user = get_object_or_404(Profile, id=id)
    
    if Friend.objects.are_friends(request.user, user):
        is_friend=True
    
    elif Block.objects.is_blocked(request.user, user) or Block.objects.is_blocked(user, request.user) or user.public==False:
        return redirect('main.get_user',username=user.username)
        
    if is_friend or user.public==True :
        
        friend_list = Friend.objects.friends(user)
        num_friends = len(friend_list)
        
        page = request.GET.get('page', 1)
        paginator = Paginator(friend_list, 12)
        try:
            friends = paginator.page(page)
        except PageNotAnInteger:
            friends = paginator.page(1)
        except EmptyPage:
            friends = paginator.page(paginator.num_pages)
        
        if FriendshipRequest.objects.filter(from_user=user,to_user=request.user).exists():
            requested=True   
        elif FriendshipRequest.objects.filter(from_user=request.user,to_user=user).exists():
            pending=True
        else:
            addfriend=True  
            
        context = {
            'friends_active':'-active',
            'user':user,
            'is_friend':is_friend,
            'friends':friends,
            'requested':requested,
            'addfriend':addfriend,
            'pending':pending,
            'num_friends':num_friends,
        }

        return render(request,  'main/userhome/view_friends.html', context)
    
    else:
        return redirect('main.get_user',username=user.username)
        

@login_required
def get_user_posts(request):
    
    is_friend = requested = pending = addfriend = False
    
    hid = request.GET.get('id', None)
    id = hashids_user.decode(hid)[0]
    
    user = get_object_or_404(Profile, id=id)
    
    if  Friend.objects.are_friends(request.user, user):
        is_friend=True
        
    elif Block.objects.is_blocked(user, request.user) or Block.objects.is_blocked(request.user, user) or user.public==False:
        return redirect('main.get_user',username=user.username)
    
        
    if is_friend or user.public==True:
        
        post_list = user.post_set.order_by('last_edited')
        num_posts = post_list.count()
        
        page = request.GET.get('page', 1)
        paginator = Paginator(post_list, 6)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            friends = paginator.page(paginator.num_pages)
        
        if FriendshipRequest.objects.filter(from_user=user,to_user=request.user).exists():
            requested=True   
        elif FriendshipRequest.objects.filter(from_user=request.user,to_user=user).exists():
            pending=True
        else:
            addfriend=True  
            
        context = {
            'posts_active':'-active',
            'user':user,
            'is_friend':is_friend,
            'posts':posts,
            'num_posts':num_posts,
            'requested':requested,
            'addfriend':addfriend,
            'pending':pending,
        }

        return render(request,  'main/userhome/view_posts.html', context)
    
    elif user.public==False:
        return redirect('main.get_user',username=user.username)

@login_required
def get_user_blogs(request):
    
    is_friend = requested = pending = addfriend = False
    
    hid = request.GET.get('id', None)
    id = hashids_user.decode(hid)[0]
    
    user = get_object_or_404(Profile, id=id)
    
    if  Friend.objects.are_friends(request.user, user):
        is_friend=True
    
    elif Block.objects.is_blocked(user, request.user) or Block.objects.is_blocked(request.user, user) or user.public==False:
        return redirect('main.get_user',username=user.username)
        
    if is_friend or user.public==True:
        
        blog_list = user.blog_set.order_by('last_edited')
        num_blogs = blog_list.count()
        
        page = request.GET.get('page', 1)
        paginator = Paginator(blog_list, 6)
        try:
            blogs = paginator.page(page)
        except PageNotAnInteger:
            blogs = paginator.page(1)
        except EmptyPage:
            blogs = paginator.page(paginator.num_pages)
        
        if FriendshipRequest.objects.filter(from_user=user,to_user=request.user).exists():
            requested=True   
        elif FriendshipRequest.objects.filter(from_user=request.user,to_user=user).exists():
            pending=True
        else:
            addfriend=True
            
        context = {
            'blogs_active':'-active',
            'user':user,
            'is_friend':is_friend,
            'blogs':blogs,
            'num_blogs':num_blogs,
            'requested':requested,
            'addfriend':addfriend,
            'pending':pending,
        }

        return render(request,  'main/userhome/view_blogs.html', context)
    
    elif user.public==False:
        return redirect('main.get_user',username=user.username)
        
        
@login_required
def get_user_courses(request):
    
    is_friend = requested = pending = addfriend = False
    
    hid = request.GET.get('id', None)
    id = hashids_user.decode(hid)[0]
    
    user = get_object_or_404(Profile, id=id)
    
    if  Friend.objects.are_friends(request.user, user):
        is_friend=True
    
    elif Block.objects.is_blocked(user, request.user) or Block.objects.is_blocked(request.user, user) or user.public==False:
        return redirect('main.get_user',username=user.username)
        
    if is_friend or user.public==True:
        
        course_list = user.courses.order_by('course_year')
        num_courses = course_list.count()
        
        page = request.GET.get('page', 1)
        paginator = Paginator(course_list, 12)
        try:
            courses = paginator.page(page)
        except PageNotAnInteger:
            courses = paginator.page(1)
        except EmptyPage:
            courses = paginator.page(paginator.num_pages)
            
        if FriendshipRequest.objects.filter(from_user=user,to_user=request.user).exists():
            requested=True   
        elif FriendshipRequest.objects.filter(from_user=request.user,to_user=user).exists():
            pending=True
        else:
            addfriend=True
              
        context = {
            'courses_active':'-active',
            'user':user,
            'is_friend':is_friend,
            'courses':courses,
            'num_courses':num_courses,
            'requested':requested,
            'addfriend':addfriend,
            'pending':pending,
        }

        return render(request, 'main/userhome/view_courses.html', context)
    
    elif user.public==False:
        return redirect('main.get_user',username=user.username)
    

@login_required
def report_object(request,reporter_id):
    
    obj_type = request.GET.get('t',None)
    obj_id = request.GET.get('hid', None)
    user_id = hashids_user.decode(hid)[0]
    if Profile.objects.filter(id=user_id).exists():
        reporter = Profile.objects.get(id=user_id)
        
        if request.method == 'POST':
            if obj_type == 'u':
                reprt = 
            if obj_type == 'p':
                pass
            if obj_type == 'cmnt':
                pass
            if obj_type == 'bz':
                pass
            if obj_type == 'bzrply':
                pass
            if obj_type == 'blg':
                pass
            if obj_type == 'blgrply':
                pass
            if obj_type == 'cr':
                pass