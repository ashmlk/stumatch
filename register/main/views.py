from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.shortcuts import render, redirect
from .forms import (
    SignUpForm, EditProfileForm, PasswordResetForm, 
    ConfirmPasswordForm, ReportUserForm, ReportPostForm, 
    ReportCommentForm, ReportBuzzForm, ReportBuzzReplyForm, 
    ReportBlogForm, ReportBlogReplyForm, ReportCourseReviewForm, 
    ContactForm, SetUniversityForm
    )
from django.views.generic.edit import UpdateView
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from hashids import Hashids
from .models import BookmarkBlog, BookmarkBuzz, BookmarkPost, Profile
from home.models import Post, Buzz, Blog, Review, Comment, BlogReply, BuzzReply
from django.db.models import Q, F, Count, Avg, FloatField, Max, Min, Case, When
from django.http import JsonResponse
from taggit.models import Tag
from friendship.models import Friend, Follow, Block, FriendshipRequest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime, timezone
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from main.decorators import confirm_password
from notifications.signals import notify
from django.core.mail import send_mail
from django.contrib.auth.decorators import user_passes_test
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from register.settings.production import sg
from django.template import RequestContext
from django.contrib.contenttypes.models import ContentType
from allauth.account.utils import *
import time


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

def cookies_html(request):
    
    return render(request, 'web_docs/cookies/index.html')

def terms_html(request):
    
    return render(request, 'web_docs/terms/index.html')

def about_html(request):
    
    return render(request, 'web_docs/about/index.html')

def handle_404(request, exception):
        context = {}
        response = render(request, "404.html", context=context)
        response.status_code = 404
        return response

def handle_403(request, exception):
        context = {}
        response = render(request, "403.html", context=context)
        response.status_code = 403
        return response

def handle_400(request, exception):
        context = {}
        response = render(request, "400.html", context=context)
        response.status_code = 400
        return response

def handle_500(request):
        context = {}
        response = render(request, "500.html", context=context)
        response.status_code = 500
        return response

def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            sender_name = form.cleaned_data['name']
            sender_email = form.cleaned_data['email']
            message_text = "Name: {0}\nEmail: {1}\n\n Sent you a new contact message:\n\n{2}".format(sender_name, sender_email, form.cleaned_data['message']) #message to be sent to contact@domain.com 
            message = Mail(
                from_email='JoinCampus NoReply <no-reply@joincampus.ca>',
                to_emails='contact@joincampus.ca',
                subject='User Contact Submitted',
                plain_text_content = message_text
                )
            try:
                response = sg.send(message)
            except Exception as e:
                print(e)   
            messages.success(request, 'Successfully submitted your form. Thanks for getting in touch with us!')
            form = ContactForm
            return redirect('main:contact-us')
    else:
        form = ContactForm

    return render(request, 'web_docs/contact/contact_us.html', {'form': form})

@login_required
def get_notifications(request):
     
    notifications_list = request.user.notifications.order_by('-timestamp')

    read_count = str(request.user.notifications.unread().count()) + " new notifications " if request.user.notifications.read().count() > 1 else 'no new notifications'
    
    request.user.notifications.mark_all_as_read() # when user visits page mark all notifications as read
    
    page = request.GET.get('page', 1)
    paginator = Paginator(notifications_list, 15)
    try:
        notifications = paginator.page(page)
    except PageNotAnInteger:
        notifications = paginator.page(1)
    except EmptyPage:
        notifications = paginator.page(paginator.num_pages)
    
    context = {
        'notifications':notifications,
        'read_count':read_count,
        }
    
    return render(request, 'main/notifications/notifications_list.html', context)


@login_required
def delete_notification(request):
    data = dict()
    """marking notification(s) as read"""
    notice_id = request.GET.get("notice_id", None)
    if notice_id: # if notice_id exists means one notification is being updated
        request.user.notifications.get(id=notice_id).delete()
        data['read_count'] =  str(request.user.notifications.unread().count()) + " new notifications " if request.user.notifications.read().count() > 1 else 'no new notifications'
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
    storage = messages.get_messages(request)
    for _ in storage:
        pass
    for _ in list(storage._loaded_messages):
        del storage._loaded_messages[0]
    return redirect('main:user_login')
    
def signup(request):
    
    if request.user.is_authenticated:
        if request.user.is_active:
            return redirect('home:home')     
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            storage = messages.get_messages(request)
            for _ in storage:
                pass
            for _ in list(storage._loaded_messages):
                del storage._loaded_messages[0]
            user = form.save(commit=False)  
            user.is_active = False
            user.save()
            send_email_confirmation(request, user, True)
            return redirect('main:user_login')
    else:
        form = SignUpForm()
    return render(request, 'main/signup.html', {'form': form})

#@user_passes_test(lambda user: not user.username, login_url='/home/', redirect_field_name=None)
def user_login(request):
    
    if request.user.is_authenticated:
        return redirect('home:home')   
    #message = ''
    if request.method == 'POST':
        storage = messages.get_messages(request)
        for _ in storage:
            pass
        for _ in list(storage._loaded_messages):
            del storage._loaded_messages[0]
        username = request.POST.get('username')
        password = request.POST.get('password')
        vp = request.POST.get('vp', None)
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                storage = messages.get_messages(request)
                for _ in storage:
                    pass
                for _ in list(storage._loaded_messages):
                    del storage._loaded_messages[0]
                return redirect('home:home')
            else:
                return HttpResponse('Account is disabled')
        else:
            messages.error(request,'Sorry, the username or password you entered is not correct')
            if vp == 'md':
                return redirect('login') 
            else:
                return redirect('main:user_login')
              
    return render(request, 'main/user_login.html')
    
def update_user_email_on_verification(request):
    
    data = dict()
    user = request.user
    if request.method == "POST":
        new_email = request.POST.get('email')
        user.add_email_address(request, new_email)
        return render(request, 'account/custom_snippets/verification_sent.html', {'email': new_email})

    else:
        context = {
            'email':''
        }
        data['form'] = render_to_string('account/email/update_email.html',context,request=request)
    
    return JsonResponse(data)
        
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            storage = messages.get_messages(request)
            for _ in storage:
                pass
            for _ in list(storage._loaded_messages):
                del storage._loaded_messages[0]
            messages.success(request, 'Your password was successfully updated.')
            return redirect('main:change-password')
        else:
            storage = messages.get_messages(request)
            for _ in storage:
                pass
            for _ in list(storage._loaded_messages):
                del storage._loaded_messages[0]
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form': form,
        'privacy_active':'setting-link-active',
    }
    return render(request, 'main/settings/change_password.html', context)

@login_required
def edit_profile(request):
        
    context = {
        'account_active':'setting-link-active'
        }
    return render(request, 'main/settings/edit_profile.html', context)

@login_required
def edit_profile_data(request):
    
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('main:settings-edit')
    else:
        form = EditProfileForm(instance=request.user)
        
    context = {
        'form':form,
        'account_active':'setting-link-active'
        }
    return render(request, 'main/settings/edit_profile_data.html', context)


@login_required
def edit_profile_university(request):
    

    if request.method == 'POST':
        form  = SetUniversityForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('main:settings-edit')
        else:
            data['form_valid'] = False
    else:
        form = SetUniversityForm(instance=request.user)
    context = {
        'form':form,
    }
    return render(request, 'main/settings/edit_profile_university.html',context)   

@login_required
def add_university(request):
    
    data = dict()
    success_url = request.GET.get('success_url','home')
    if request.method == 'POST':
        form  = SetUniversityForm(request.POST, instance=request.user)
        if form.is_valid():
            if len(request.user.university) > 1:
                request.session['no_university'] = False
            data['form_valid'] = True
            form.save()
        else:
            data['form_valid'] = False
    else:
        form = SetUniversityForm(instance=request.user)
    context = {
        'form':form,
        'su':success_url
    }
    data['html_form'] = render_to_string('main/settings/university_update.html',context,request=request)   
    return JsonResponse(data)

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
                try:
                    image = request.FILES['cropped_image']
                    user.image = image
                    user.save()
                    data['new_url'] = reverse('main:update-image', kwargs={'hid':request.user.get_hashid()})
                    return JsonResponse(data)
                except Exception as e:
                    pass  
           
    if request.user.image.url != '/media/defaults/user/default_u_i.png':
        image_not_default = True
    else:
        image_not_default = False


    context = {
        'image_not_default':image_not_default,
        'account_active':'setting-link-active'
        }
    return render(request, 'main/settings/edit_profile_image.html', context)

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
                user.save()
                image_not_default = False   
                img_url = user.image.url
        data['new_url'] = reverse('main:update-image', kwargs={'hid':request.user.get_hashid()})
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
        #last_login_utc = request.user.last_login  
        #date_joined_utc = request.user.date_joined
        #last_login = last_login_utc.replace(tzinfo=timezone.utc).astimezone(tz=None)
        #date_joined = date_joined_utc.replace(tzinfo=timezone.utc).astimezone(tz=None)
        
        last_login = request.user.get_last_login_local()
        date_joined = request.user.get_date_joined_local()
        
        context = {
            'last_login':last_login,
            'date_joined':date_joined,
            'privacy_active':'setting-link-active',
        }
        
        return render(request,'main/settings/login_info.html', context)
        
@login_required
def deletion_menu(request):
    
    if request.user.is_authenticated:
        storage = messages.get_messages(request)
        for _ in storage:
            pass
        for _ in list(storage._loaded_messages):
            del storage._loaded_messages[0]
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
    
    o = request.GET.get('o','posts')
    post_active = blog_active =  ''
    context = {}
    
    user = request.user
    if o == 'posts':
        post_active = '-active'
        bookmarked_posts = user.bookmarkpost_set.all()
        context = {
        'bookmarked_posts':bookmarked_posts,
        'post_active':post_active
        }
    elif o == 'blogs':
        blog_active = '-active'
        bookmarked_blogs = user.bookmarkblog_set.all()
        context = {
        'bookmarked_blogs':bookmarked_blogs,
        'blog_active':blog_active
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
        actor_type = ContentType.objects.get_for_model(Profile)
        target_type = ContentType.objects.get_for_model(FriendshipRequest)
        action = int(s)
        is_friend=None
        if action == 0:  # to accept friend request sent by other_user to user
            fr = FriendshipRequest.objects.get(from_user=other_user,to_user=user)
            try:
                message = "CON_FRRE" + "has sent you a friend request"
                user.notifications.filter(actor_content_type__id=actor_type.id, actor_object_id=other_user.id, target_content_type__id=target_type.id, \
                target_object_id=fr.id, recipient=user, verb=message).delete()
            except Exception as e:
                print(e.__class__)   
                print("There was an issue with deleting a friend request")           
            fr.accept()
            is_friend=True
            if other_user.get_friendrequestaccepted_notify: 
                message = "CON_FRRE" + "has accepted your friend request"
                notify.send(sender=user, recipient=other_user, verb=message, target=fr)
                    
        elif action == 1:  # to cancel a request sent by other user to user
            if FriendshipRequest.objects.filter(from_user=other_user,to_user=user).exists():
                fr = FriendshipRequest.objects.get(from_user=other_user,to_user=user)
                try:
                    message = "CON_FRRE" + "has sent you a friend request"
                    user.notifications.filter(actor_content_type__id=actor_type.id, actor_object_id=other_user.id, target_content_type__id=target_type.id, \
                    target_object_id=fr.id, recipient=user, verb=message).delete()
                except Exception as e:
                    print(e.__class__)   
                    print("There was an issue with deleting a friend request")                  
                fr.cancel()        
                
        elif action == 2: # unblock a user and set the option to option add friend
            if Block.objects.is_blocked(user, other_user):
                Block.objects.remove_block(user,other_user)
                
        elif action == 3: # cancel pending request from user
            
            if FriendshipRequest.objects.filter(from_user=user,to_user=other_user).exists():
                fr = FriendshipRequest.objects.get(from_user=user,to_user=other_user)
                try:
                    message = "CON_FRRE" + "has sent you a friend request"
                    other_user.notifications.filter(actor_content_type__id=actor_type.id, actor_object_id=user.id, target_content_type__id=target_type.id, \
                    target_object_id=fr.id, recipient=other_user, verb=message).delete()
                except Exception as e:
                    print(e.__class__)   
                    print("There was an issue with deleting a friend request") 
                fr.cancel()
                
            if FriendshipRequest.objects.filter(from_user=other_user,to_user=user).exists():
                fr = FriendshipRequest.objects.get(from_user=other_user,to_user=user)
                
                try:
                    message = "CON_FRRE" + "has sent you a friend request"
                    other_user.notifications.filter(actor_content_type__id=actor_type.id, actor_object_id=other_user.id, target_content_type__id=target_type.id, \
                    target_object_id=fr.id, recipient=other_user, verb=message).delete()
                except Exception as e:
                    print(e.__class__)   
                    print("There was an issue with deleting a friend request") 
                    
                fr.cancel()
                
            is_friend=False
            
        friends_list = Friend.objects.friends(request.user)
        pending_requests = Friend.objects.sent_requests(user=request.user)
        requests = Friend.objects.requests(user=request.user)
        total_friends = len(friends_list)
        total_requests = len(requests)
        total_pending = len(Friend.objects.sent_requests(user=request.user))
        request.session['total_friends'] = total_friends
        request.session['total_requests'] = total_requests
        request.session['total_pending'] = total_pending
        
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
            if not FriendshipRequest.objects.filter(from_user=user,to_user=other_user).exists():
                Friend.objects.add_friend(user, other_user) # send a friend request to other_user
                pending = True
                if other_user.get_friendrequest_notify:
                    fr = FriendshipRequest.objects.get(from_user=user,to_user=other_user)
                    message = "CON_FRRE" + "has sent you a friend request"
                    notify.send(sender=user, recipient=other_user, verb=message, target=fr)
                
        friends_list = Friend.objects.friends(request.user)
        requests = Friend.objects.requests(user=request.user)
        total_friends = len(friends_list)
        total_requests = len(requests)
        request.session['total_friends'] = total_friends
        request.session['total_requests'] = total_requests
        
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
    
    data = dict()
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
    friends= Friend.objects.friends(request.user)
    friends_list = Profile.objects.filter(id__in=[u.id for u in friends])
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
        'total_blocked':total_blocked,
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
    total_blocked = request.session.get('total_blocked')
       
    context = {
        'friend_requests':friend_requests,
        'mutuals_request':mutual_friends_with_requests,
        'total_friends':total_friends,
        'request_active':'active',
        'total_friends':total_friends,
        'total_requests':total_requests,
        'total_pending':total_pending,
        'total_blocked':total_blocked
    }
    
    return render(request, 'main/friends/friend_requests.html', context)

@login_required
def friend_pending_requests(request):
    
    lister = Friend.objects.sent_requests(user=request.user)
    ids = [l.to_user.id for l in lister] 
    user_list = Profile.objects.filter(id__in=ids)
    
    total_friends = request.session.get('total_friends')
    total_requests = request.session.get('total_requests')
    total_pending = request.session.get('total_pending')
    total_blocked = request.session.get('total_blocked')
    
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
        'total_blocked':total_blocked,
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

    if uni and pro:
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
    
    num_obj = request.user.favorite_post_tags.count() + request.user.favorite_blog_tags.count()
    if num_obj < 1:
        s= "Tag"
    if o == 'post':
        tags = request.user.favorite_post_tags.all()
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
        blnum = user.blog_set.count()
        cnum = user.courses.count()
        courses = user.courses.distinct('course_code','course_instructor')[:4]
        post_ids = Post.objects.get_top_for_user(user=user)
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(post_ids)])
        posts = Post.objects.select_related("author").filter(id__in=post_ids).order_by(-preserved)[:4]
        blogs = user.blog_set.order_by('-last_edited')[:4]
        friends = Friend.objects.friends(user)
        num_friends = len(friends)
        context = {
            'user':user,
            'pnum':pnum,
            'blnum':blnum,
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

        post_list = user.post_set.order_by('-last_edited')
        page = request.GET.get('page_posts', 1)
        paginator = Paginator(post_list, 1)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        
        blogs = user.blog_set.order_by('-last_edited')[:5]

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

        post_list = user.post_set.order_by('-last_edited')
        page = request.GET.get('page_posts', 1)
        paginator = Paginator(post_list, 1)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        
        blogs = user.blog_set.order_by('-last_edited')[:5]

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
        
        post_list = user.post_set.order_by('-last_edited')
        num_posts = post_list.count()
        
        page = request.GET.get('page', 1)
        paginator = Paginator(post_list, 8)
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
        paginator = Paginator(blog_list, 8)
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
        paginator = Paginator(course_list, 8)
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
    
    data = dict()
    
    obj_type = request.GET.get('t',None)
    obj_id = request.GET.get('hid', None)
    user_id = hashids_user.decode(reporter_id)[0]
    if Profile.objects.filter(id=user_id).exists():
        reporter = Profile.objects.get(id=user_id)
        
        if request.method == 'POST':
            if obj_type == 'u':
                form = ReportUserForm(request.POST)
                if form.is_valid():
                    if Profile.objects.filter(id=hashids_user.decode(obj_id)[0]).exists():
                        report = form.save(False)
                        report.reporter = reporter
                        report.reported_obj =  Profile.objects.get(id=hashids_user.decode(obj_id)[0])
                        report.save()
            elif obj_type == 'p':
                form = ReportPostForm(request.POST)
                if form.is_valid():
                    if Post.objects.filter(id=hashids.decode(obj_id)[0]).exists():
                        report = form.save(False)
                        report.reporter = reporter
                        report.reported_obj =  Post.objects.get(id=hashids.decode(obj_id)[0])
                        report.save()
            elif obj_type == 'cmnt':
                form = ReportCommentForm(request.POST)
                if form.is_valid():
                    if Comment.objects.filter(id=hashids.decode(obj_id)[0]).exists():
                        report = form.save(False)
                        report.reporter = reporter
                        report.reported_obj =  Comment.objects.get(id=hashids.decode(obj_id)[0])
                        report.save()
            elif obj_type == 'blg':
                form = ReportBlogForm(request.POST)
                if form.is_valid():
                    if Blog.objects.filter(id=hashids.decode(obj_id)[0]).exists():
                        report = form.save(False)
                        report.reporter = reporter
                        report.reported_obj = Blog.objects.get(id=hashids.decode(obj_id)[0])
                        report.save()
            elif obj_type == 'blgrply':
                form = ReportBlogReplyForm(request.POST)
                if form.is_valid():
                    if BlogReply.objects.filter(id=hashids.decode(obj_id)[0]).exists():
                        report = form.save(False)
                        report.reporter = reporter
                        report.reported_obj =  BlogReply.objects.get(id=hashids.decode(obj_id)[0])
                        report.save()
            elif obj_type == 'cr':
                form = ReportCourseReviewForm(request.POST)
                if form.is_valid():
                    if Review.objects.filter(id=hashids.decode(obj_id)[0]).exists():
                        report = form.save(False)
                        report.reporter = reporter
                        report.reported_obj =  Review.objects.get(id=hashids.decode(obj_id)[0])
                        report.save()
            
            data['user_valid'] = True           
        
        else:
            
            msg_dict = {
                'u':'To help us understand the problem what is the issue with this profile?',
                'p':'To help us understand the problem, what is the issue with this post?',
                'cmnt':'To help us understand the problem, what is the issue with this comment?',
                'blg':'To help us understand the problem, what is the issue with this blog?',
                'blgrply':'To help us understand the problem, what is the issue with this reply?',
                'cr':'What is the issue with this review?'
            }
            
            form_dict = {
                'u':ReportUserForm,'p':ReportPostForm,'cmnt':ReportCommentForm,'blg':ReportBlogForm,'blgrply':ReportBlogReplyForm,'cr':ReportCourseReviewForm   
            }
                
            context = {
                'form':form_dict[obj_type],
                'message': msg_dict[obj_type],
                'obj_type':obj_type,
                'obj_id':obj_id,
                'user_valid':True
            }
            
            data['html_form'] =  render_to_string('report/report_form.html',context,request=request)  
    else:
        
        context = {
            'error_message':'Sorry there seems to be an issue with your request',
            'obj_type':obj_type,
            'obj_id':obj_id,
            'user_valid':False
            }
        
        data['user_valid'] = False
        data['html_form'] =  render_to_string('report/report_form.html',context,request=request) 
    
    return JsonResponse(data)


def get_user_mentions(request):
    
    text = request.GET.get('q', None)
    top_users = Profile.objects.search_topresult(search_text=text)[:10]
    top_users_json = list(top_users[:10].values('first_name','last_name','username','image'))
    for value in top_users_json:
        newURL = settings.MEDIA_URL
        newURL += value['image']
        value['image'] = newURL
    return JsonResponse(top_users_json, safe=False)

    
    