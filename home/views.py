from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views import View
from django.utils import timezone
from django.db.models import Q, F, Count, Avg, FloatField, Max, Min, Case, When
from hashids import Hashids
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, RedirectView
from django.forms import modelformset_factory 
from .models import Post, Comment, Images, Course, Review, Buzz, BuzzReply, Blog, BlogReply, CourseList, CourseListObjects
from main.models import Profile, SearchLog
from .forms import PostForm, CommentForm, CourseForm, CourseEditForm, ImageForm, ReviewForm, BuzzForm, BuzzReplyForm, BlogForm, BlogReplyForm, CourseListForm, CourseListObjectsForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .post_guid import uuid2slug, slug2uuid
from django.urls import reverse
import datetime
from datetime import timedelta
from django.db.models.functions import Now
from django.utils.timezone import make_aware
from dal import autocomplete
from taggit.models import Tag
from friendship.models import Friend, Follow, Block, FriendshipRequest
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.core.cache import cache
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, TrigramSimilarity
from notifications.signals import notify
import json
from home.algo import get_uni_info 
from itertools import chain
from home.templatetags.ibuilder import num_format

# Max number of courses can have in every semester
MAX_COURSES = 7

hashids = Hashids(salt='v2ga hoei232q3r prb23lqep weprhza9',min_length=8)

hashid_list = Hashids(salt='e5896e mqwefv0t mvSOUH b90 NS0ds90',min_length=16)

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

# main page that user see's the hope page
@login_required
def home(request):
    
    
    if len(request.user.university) < 1:
        request.session['no_university'] = True 
    
    words = []
    
    friends = Friend.objects.friends(request.user)
    
    """ get a list of users that user has blocked and save it to request.session """
    blockers_list = Block.objects.blocked(request.user)
    request.session['blockers'] = [u.id for u in blockers_list]
    
    posts_list = Post.objects.select_related('author').filter(Q(author__in=friends)|Q(author=request.user)).order_by('-last_edited')
    
    """ get hot words and tags related to posts form tags """
    tags = cache.get("tt_post")
    top_words = cache.get("trending_words_posts")
    if top_words:
        words = top_words['phrases']
    
    """ @param is_home is set to True """
    """ home.html is used in other functions, is_home changes the view """
    is_home = True
    page = request.GET.get('page', 1)
    paginator = Paginator(posts_list, 10)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    context = { 
                'posts':posts,
                'is_home':is_home,
                'tags':tags,
                'words':words,
                'home_active':'-active',
            }
    return render(request, 'home/homepage/home.html', context)

@login_required
def users_posts(request):
    
    posts = request.user.post_set.order_by('-last_edited')
    context = { 'posts':posts, 'post_active':'-active' }
    return render(request, 'home/homepage/user_byyou.html', context)

@login_required
def users_blogs(request):
    
    blogs = request.user.blog_set.order_by('-last_edited')
    context = {'blogs':blogs, 'blog_active':'-active' }
    return render(request, 'home/homepage/user_byyou.html', context)

@login_required
def hot_posts(request):
    
    blockers_id = words = post_list_ids = posts_list = []
    
    """ @param preserved keeps the order of the hot posts """
    posts_list_ids = cache.get("hot_posts")
    blockers_id = request.session.get('blockers')
    
    if post_list_ids:
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(posts_list_ids)])
        posts_list = Post.objects.select_related("author").filter(id__in=posts_list_ids).exclude(author__id__in=blockers_id).order_by(preserved)
    
    
    """ get hot words and tags related to posts form tags """
    tags = cache.get("tt_post")
    top_words = cache.get("trending_words_posts")
    
    if top_words:
        words = top_words['phrases']
        words = words + top_words['common_words']
    
    page = request.GET.get('page', 1)
    paginator = Paginator(posts_list, 10)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = { 
                'posts':posts, 
                'hot_active':'-active',
                'tags':tags,
                'words':words,
                'is_home':True,
            }
    return render(request, 'home/homepage/home.html', context)

@login_required
def top_posts(request):
    
    blockers_id = words = post_list_ids = posts_list = []
    
    """ @param preserved keeps the order of the hot posts """
    posts_list_ids = cache.get("hot_posts")
    blockers_id = request.session.get('blockers')
    
    if post_list_ids:
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(posts_list_ids)])
        posts_list = Post.objects.select_related("author").filter(id__in=posts_list_ids).exclude(author__id__in=blockers_id).order_by(preserved)
    
    """ get hot words and tags related to posts form tags """
    tags = cache.get("tt_post")
    top_words = cache.get("trending_words_posts")
    if top_words:
        words = top_words['phrases']
        words = words + top_words['common_words']
    
    page = request.GET.get('page', 1)
    paginator = Paginator(posts_list, 10)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
        
    context = { 
                'posts':posts,
                'top_active':'-active',
                'tags':tags,
                'words':words,
                'is_home':True
            }
    return render(request, 'home/homepage/home.html', context)

@login_required
def uni_posts(request):
    
    words = []
    posts = None
    
    u = request.user.university 
    t = u.lower().replace(' ','_')+"_post"

    posts_list = cache.get(t)
    
    blockers_id = request.session.get('blockers')
    
    if posts_list:
        posts_list = posts_list.exclude(author__id__in=blockers_id)
        page = request.GET.get('page', 1)
        paginator = Paginator(posts_list, 10)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
    
    """ get hot words and tags related to posts form tags """
    tags = cache.get("tt_post")
    top_words = cache.get("trending_words_posts")
    if top_words:
        words = top_words['phrases']
        words = words + top_words['common_words']
    
    context = { 
                'posts':posts,
                'uni_active':'-active',
                'tags':tags,
                'words':words,
                'is_home':True
            }
    
    return render(request, 'home/homepage/home.html', context)

@cache_page(60*60*24*1)
@login_required
def top_word_posts(request):
    
    words = []
    
    if request.method == 'GET':
        word = request.GET.get('w', None)
        posts_list = Post.objects.select_related("author").filter(author__public=True, content__unaccent__icontains=word)
        page = request.GET.get('page', 1)
        paginator = Paginator(posts_list, 10)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        
        """ get hot words and tags related to posts form tags """
        tags = cache.get("tt_post")
        top_words = cache.get("trending_words_posts")
        if top_words:
            words = top_words['phrases']
            words = words + top_words['common_words']
    
        context = { 
                    'posts':posts,
                    'word':word, 
                    'is_word':True,
                    'tags':tags,
                    'words':words }
        return render(request, 'home/homepage/home.html', context)
   
@login_required
def post_create(request):
    
    data = dict()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES or None)
        if form.is_valid(): 
            post = form.save(False)
            post.author = request.user
            post.save()
            form.save_m2m()
            if request.FILES is not None:
                images = [request.FILES.get('images[%d]' % i) for i in range(0, len(request.FILES))]  
                for i in images:
                    image_instance = Images.objects.create(image=i,post=post)
                    image_instance.save()
            data['form_is_valid'] = True
            data['post'] = render_to_string('home/posts/new_post.html',{'post':post},request=request)
        else:
            data['form_is_valid'] = False
    else:
        form = PostForm  
            
    context = {
    'form':form,
	}
    data['html_form'] = render_to_string('home/posts/post_create.html',context,request=request)
    return JsonResponse(data) 


@login_required
def post_update(request, guid_url):
    data = dict()
    post = get_object_or_404(Post, guid_url=guid_url)
    if post.author == request.user:
        if request.method == 'POST':
            form = PostForm(request.POST,instance=post)
            form.instance.author = request.user
            if form.is_valid():
                form.save()
                data['form_is_valid'] = True
                data['post'] = render_to_string('home/posts/new_post.html',{'post':post},request=request) 
        else:
            form = PostForm(instance=post)
            form.instance.author = request.user
        data['html_form'] = render_to_string('home/posts/post_update.html',{'form':form},request=request)
        return JsonResponse(data)

@login_required
def post_delete(request, guid_url):
    data = dict()
    post = get_object_or_404(Post, guid_url=guid_url)
    if request.method == 'POST':
        if post.author == request.user:
            post.delete()
            data['form_is_valid'] = True
    else:
        context = {'post':post}
        data['html_form'] = render_to_string('home/posts/post_delete.html',context,request=request)
    return JsonResponse(data)

@login_required
def post_detail(request, guid_url):
    
    data = dict()
    post = get_object_or_404(Post, guid_url=guid_url)
    comment_list = post.comments.filter(reply=None)
    if request.method == 'POST':
        is_reply = None
        form = CommentForm(request.POST or None)
        if form.is_valid():
            comment = form.save(False)
            reply_id = request.POST.get('comment_id')
            comment_qs = None
            if reply_id: # if reply_id exists it means the comment is a reply
                comment_qs = Comment.objects.get(id=reply_id)
                is_reply = True
                data['is_reply'] = is_reply
                description = "Reply: " + comment_qs.body
                if request.user != comment_qs.name:
                    if comment_qs.name.get_notify and comment_qs.name.get_post_notify_all and comment_qs.name.get_post_notify_comments:
                        message_comment = "CON_POST" + " replied to your comment on " + post.author.get_full_name() + "'s post." # message comment is sent to the parent comment
                        notify.send(sender=request.user, recipient=comment_qs.name, verb=message_comment, description=description, target=post, action_object=comment_qs)
                if comment_qs.name != post.author:
                    if post.author.get_notify and post.author.get_post_notify_all and post.author.get_post_notify_comments:
                        message_post = "CON_POST" + " replied to a comment on your post." # message_post is sent to the post author of the reply's parent comment
                        notify.send(sender=request.user, recipient=post.author, verb=message_post, description=description, target=post, action_object=comment_qs)
 
            comment.name = request.user
            comment.post = post
            comment.reply = comment_qs
            comment.save()
            if comment.name != post.author:
                if post.author.get_notify and post.author.get_post_notify_all and post.author.get_post_notify_comments:
                    message = "CON_POST" + " commented on your post." # message to send to post author when user comments on their post
                    description = "Comment: " + comment.body
                    notify.send(sender=request.user, recipient=post.author, verb=message, description=description, target=post, action_object=comment)
        else:
            data['is_valid'] = False
        if is_reply:
            form = CommentForm()
            context = { 'guid_url':post.guid_url,
                        'reply':comment,
                        'form':form }
            data['reply'] = render_to_string('home/posts/post_comment_reply_new.html',context,request=request)
        else:
            form = CommentForm()
            context = { 'guid_url':post.guid_url,
                        'comment':comment,
                        'form':form }
            data['comment'] = render_to_string('home/posts/post_comment_new.html',context,request=request)
        return JsonResponse(data)
    
    else:
        form = CommentForm()
    guid_url = post.guid_url
    comment_count = post.comment_count()
    page = request.GET.get('page', 1)
    paginator = Paginator(comment_list, 10)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)
    context = {'post':post,
                'form':form,
                'comments':comments,
                'comment_count':comment_count,
                'guid_url':guid_url,
                }

    return render(request,'home/posts/post_detail.html',context)
    

@login_required
def post_like(request,guid_url):
    data = dict()
    post = get_object_or_404(Post, guid_url=guid_url)
    user = request.user
    if request.method == 'POST':   
        if post.likes.filter(id=user.id).exists():
            post.likes.remove(user)
        else:
            post.likes.add(user)
            if user != post.author:
                if post.author.get_notify and post.author.get_post_notify_all and post.author.get_post_notify_likes:
                    message = "CON_POST" + " liked your post." # message to be sent to post author
                    notify.send(sender=user, recipient=post.author, verb=message, target=post)
        data['likescount'] = post.likes.count()
        data['post_likes'] = render_to_string('home/posts/likes.html',{'post':post},request=request)
        return JsonResponse(data)
        

@login_required
def comment_like(request,guid_url,hid):
    data = dict()
    guid_url = guid_url
    id =  hashids.decode(hid)[0]
    comment = get_object_or_404(Comment, id=id)
    user = request.user
    if request.method == 'POST':    
        if comment.likes.filter(id=user.id).exists():
            comment.likes.remove(user)
        else:
            comment.likes.add(user)
            try:
                if user != comment.name:
                    if comment.name.get_notify and comment.name.get_post_notify_all and comment.name.get_post_notify_comments:
                        message = "CON_POST" + " liked your comment on " + comment.post.author.get_full_name() + "'s post."
                        description = comment.body
                        notify.send(sender=user, recipient=comment.name, verb=message, description=description, target=comment.post, action_object=comment)
                if user != comment.post.author:
                    if comment.post.author.get_notify and comment.post.author.get_post_notify_all and comment.post.author.get_post_notify_comments:
                        message = "CON_POST" + " liked a comment on your post"
                        description = comment.body
                        notify.send(sender=user, recipient=comment.post.author, verb=message, description=description, target=comment.post, action_object=comment)
            except:
                print("error in sending notification to on post-comment-like --- " + str(comment.name.id) + str(comment.post.author))
                
        data['comment'] = render_to_string('home/posts/comment_like.html',{'comment':comment,'guid_url':guid_url},request=request)
        return JsonResponse(data)

@login_required
def comment_delete(request,hid):
    data=dict()
    id =  hashids.decode(hid)[0]
    comment=get_object_or_404(Comment,id=id)
    if request.method=="POST":
        if comment.name==request.user or request.user == comment.post.author:
            comment.delete()
            data['form_is_valid'] = True
    else:
        context = {'comment':comment}
        data['html_form'] = render_to_string('home/posts/comment_delete.html',context,request=request)
    return JsonResponse(data)
            
""" Method for returning a list of all users who liked a post """ 
@login_required
def post_like_list(request, guid_url):
    data = dict()
    post = get_object_or_404(Post, guid_url=guid_url)
    post_likes_list = post.likes.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(post_likes_list , 10)
    try:
        post_likes = paginator.page(page)
    except PageNotAnInteger:
        post_likes = paginator.page(1)
    except EmptyPage:
        post_likes = paginator.page(paginator.num_pages)
    
    data['list'] = render_to_string('home/posts/user_like_list.html',{'post_likes':post_likes, 'post':post},request=request)
    data['html'] = render_to_string('home/posts/post_like_list.html',{'post_likes':post_likes, 'post':post},request=request)
    return JsonResponse(data)

""" Method for returning a list of all users who commented on a post """
@login_required
def post_comment_list(request, guid_url):
    
    data = dict()
    post = get_object_or_404(Post, guid_url=guid_url)
    
    page = request.GET.get('page', 1)
    post_comment_list = post.comments.all()
    
    paginator = Paginator(post_comment_list , 10)
    try:
        post_comments = paginator.page(page)
    except PageNotAnInteger:
        post_comments = paginator.page(1)
    except EmptyPage:
        post_comments = paginator.page(paginator.num_pages)
  
    data['list'] = render_to_string('home/posts/user_comment_list.html',{'post_comments':post_comments, 'post':post},request=request)
    data['html'] = render_to_string('home/posts/post_comment_list.html',{'post_comments':post_comments, 'post':post},request=request)
    return JsonResponse(data)


@login_required
def course_menu(request):
    return render(request,'home/courses/course_menu.html',{'menu':True})

@login_required
def course_list(request):
    course_list = request.user.courses.order_by("course_code")
    
    page = request.GET.get('page', 1)
    paginator = Paginator(course_list , 7)
    try:
        courses = paginator.page(page)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
         courses = paginator.page(paginator.num_pages)
    context = { 'courses':courses }
    return render(request,'home/courses/course_list.html',context)

@login_required
def courses_instructor(request,par1,par2):
    instructor_rating = -1
    courses = Course.objects.filter(course_instructor_slug=par2,course_university_slug=par1).order_by('course_code','course_instructor_slug','course_university_slug').distinct('course_code','course_instructor_slug','course_university_slug')
    try:
        instructor_rating = Course.objects.instructor_average_voting(ins=courses.first().course_instructor, ins_fn=courses.first().course_instructor_fn, university=courses.first().course_university)
    except:
        message = "Issue with getting instructor rating for: " + courses.first().course_instructor_fn.capitalize() + " " + courses.first().course_instructor.capitalize() + " at " + courses.first().course_university
        print(message)
    context = {
         'courses':courses,
         'instructor':courses.first().course_instructor_fn.capitalize() + " " + courses.first().course_instructor.capitalize(),
         'university':courses.first().course_university,
         'instructor_rating':instructor_rating
         }
    return render(request,'home/courses/instructor_course_list.html',context)

@login_required
def course_add(request):
    if request.method == "POST":
        form = CourseForm(request.POST or None)
        if form.is_valid():
            course = form.save(False)
            code = course.course_code.upper().replace(' ', '')
            uni = course.course_university.strip().lower()
            ins_fn = course.course_instructor_fn.strip().lower()
            ins = course.course_instructor.strip().lower()
            has_course = request.user.courses.filter(course_code=code,course_instructor_fn__iexact=ins_fn, course_instructor__iexact=ins,course_year=course.course_year,\
                course_university__iexact=uni,course_semester=course.course_semester).exists()
            max_reached =  request.user.courses.filter(course_year=course.course_year,course_university__iexact=uni,course_semester=course.course_semester).count()
            course_exists = Course.objects.filter(course_code=code,course_instructor_fn__iexact=ins_fn, course_instructor__iexact=ins,course_year=course.course_year,\
                course_university__iexact=uni,course_semester=course.course_semester,course_difficulty=course.course_difficulty).exists()
            if max_reached > 7:
                form = CourseForm
                message = "You have reached maximum number of courses per semester for the " + course.sem + " semester in "+ course.course_year 
                context = {
                    'form':form,
                    'message': message,
                }
                return render(request,'home/courses/course_add.html', context)  
            elif has_course:
                form = CourseForm
                message = "It's seems you have already added this course. Please try again."
                context = {
                    'form':form,
                    'message': message,
                }
                return render(request,'home/courses/course_add.html', context)
            else:
                if course_exists:
                    c = Course.objects.filter(course_code=code,course_instructor_fn__iexact=ins_fn,course_instructor__iexact=ins,\
                            course_year=course.course_year,course_university__iexact=uni,course_semester=course.course_semester,\
                            course_difficulty=course.course_difficulty).first()
                    request.user.courses.add(c)
                else:
                    course.save()
                    request.user.courses.add(course)
                return redirect('home:course-list')
    else:     
        form = CourseForm()
        if not request.user.university == None:
            form.fields['course_university'].initial = request.user.university    
    context = {
        'form':form,
    }
    return render(request,'home/courses/course_add.html', context)


@login_required
def course_add_form_get_obj(request):
    
    data = dict()
    
    course_code_list = instructor_list = []
    
    uni = request.GET.get('u', request.user.university)
    obj = request.GET.get('o', None) #value that is initially typed in in course or instructor field
    obj0 = request.GET.get('oj', None) #value that we want without previous data - one field is blank
    obj1 = request.GET.get('ot', None) #value that we want - if set to course we are looking for course
    obj_text = request.GET.get('q', None)
    
    if obj != None and obj1 == 'instructor': #have the code and want the instructor
        instructor_list = Course.objects.values('course_instructor','course_instructor_fn')\
        .annotate(trigram=TrigramSimilarity('course_instructor', obj_text),  trigram_fn=TrigramSimilarity('course_course_instructor_fn', obj ), trigram_course=TrigramSimilarity('course_code', obj ))\
        .filter(Q(course_university__unaccent=uni), Q(trigram__gte=0.15) | Q(trigram_fn__gte=0.5), Q(trigram_course__gte=0.3))\
        .order_by('course_instructor','-trigram').distinct('course_instructor')[:7]
        
    if obj != None and obj1 == 'code': #have the instructor and want the code, obj has to be set to value of course instructor field
        course_code_list = Course.objects.values_list('course_code', flat=True)\
            .annotate(trigram=TrigramSimilarity('course_code', obj_text), trigram_ins=TrigramSimilarity('course_instructor', obj ))\
            .filter(course_university__unaccent=uni, trigram__gte=0.15,  trigram_ins__gte=0.3)\
            .order_by('course_code','-trigram').distinct('course_code')[:7]
            
    elif obj0 == 'instructor': # if obj0 is instructor no value is provided and user wants list of of instructors
        instructor_list = Course.objects.values('course_instructor','course_instructor_fn')\
            .annotate(trigram=TrigramSimilarity('course_instructor', obj_text), trigram_fn=TrigramSimilarity('course_instructor_fn', obj_text))\
            .filter(Q(course_university__unaccent=uni), Q(trigram__gte=0.1) | Q(trigram_fn__gte=0.5))\
            .order_by('course_instructor','-trigram').distinct('course_instructor')[:7]
            
    elif obj0 == 'code': # if obj0 is code then user is requesting list of course codes
        course_code_list = Course.objects.values_list('course_code', flat=True).annotate(trigram=TrigramSimilarity('course_code', obj_text)).filter(course_university__unaccent=uni, trigram__gte=0.1).\
            order_by('course_code','-trigram').distinct('course_code')[:7]
    
    course_code_list = list(course_code_list)
    instructor_list = list(instructor_list)
    
    data = {
        'ins': instructor_list,
        'code':course_code_list
    }
    
    return JsonResponse(data)

@login_required
def course_edit(request, hid):
    id =  hashids.decode(hid)[0]
    course_init = get_object_or_404(Course, id=id)
    if request.method == "POST":
        form = CourseEditForm(request.POST)
        if form.is_valid():
            course = form.save() 
            request.user.courses.add(course)  
            request.user.courses.remove(course_init)
            return redirect('home:course-list')
    else:     
        form = CourseEditForm(instance=course_init)    
    context = {
        'form':form,
        'course':course_init
    }
    return render(request,'home/courses/course_edit.html', context)   

@login_required
def course_auto_add(request, course_code,course_instructor_slug, course_university_slug):
    course = Course.objects.filter(course_instructor_slug__iexact=course_instructor_slug,course_code=course_code,course_university_slug__iexact=course_university_slug).first()
    data = dict()
    if request.method == "POST":
        form = CourseForm(request.POST or none)
        if form.is_valid():
            course = form.save(False)
            max_reached =  request.user.courses.filter(course_year=course.course_year,course_university__iexact=course.course_university,course_semester=course.course_semester).count()
            course_exists = Course.objects.filter(course_code=course.course_code,course_instructor_fn__iexact=course.course_instructor_fn,\
                                                    course_instructor__iexact=course.course_instructor,course_year=course.course_year,\
                                                        course_university__iexact=course.course_university,course_semester=course.course_semester,\
                                                            course_difficulty=course.course_difficulty, course_prof_difficulty=course.course_prof_difficulty).exists()
            if max_reached > 7:
                    data['message'] =  "You have already reached maximum number of courses per semester for the " + course.sem + " semester in "+ course.course_year  
            else:
                if course_exists:
                    c = Course.objects.filter(course_code=course.course_code,course_instructor_fn__iexact=course.course_instructor_fn,\
                                                course_instructor__iexact=course.course_instructor,course_year=course.course_year,\
                                                    course_university__iexact=course.course_university,course_semester=course.course_semester,\
                                                        course_difficulty=course.course_difficulty, course_prof_difficulty=course.course_prof_difficulty).first()
                    request.user.courses.add(c)
                else:
                    course.save()
                    request.user.courses.add(course)
                    data["message"] = "Course added successfully"
            data['form_is_valid'] = True
    else:
        empty = ''
        form = CourseForm(initial={
            'course_code':course.course_code,
            'course_instructor_fn':course.course_instructor_fn, 
            'course_instructor': course.course_instructor, 
            'course_university':course.course_university,
            'course_year': empty 
            })
        
        form.fields['course_code'].widget.attrs['readonly']  = True
        form.fields['course_instructor'].widget.attrs['readonly']  = True
        form.fields['course_instructor_fn'].widget.attrs['readonly']  = True
        form.fields['course_university'].widget.attrs['readonly']  = True
        context = {
            'form':form,
            'course':course,
        }
        data['html_form'] = render_to_string('home/courses/course_auto_add.html',context,request=request)
    return JsonResponse(data)

@login_required     
def course_remove(request, hid):
    data= dict()
    id = hashids.decode(hid)[0]
    course = get_object_or_404(Course, id=id)
    if request.method == 'POST':
        request.user.courses.remove(course)
        data['is_valid'] = True
        if request.user.courses.count() == 0:
            data['done'] = True
            return redirect('home:courses')
    else:
        context = {'course':course}
        data['html_form'] = render_to_string('home/courses/course_remove.html',context,request=request)
    return JsonResponse(data)

@login_required 
def course_vote(request, hid, code, status=None):
    data = dict()
    id = hashids.decode(hid)[0]
    course = get_object_or_404(Course, id=id)
    code = code
    
    if request.method == 'POST':
        
        if status=="like":
            if course.course_dislikes.filter(id=request.user.id).exists():
                course.course_dislikes.remove(request.user)
            course.course_likes.add(request.user)
        
        elif status=="dislike":
            if course.course_likes.filter(id=request.user.id).exists():
                course.course_likes.remove(request.user)
            course.course_dislikes.add(request.user)
            
        elif status=="rmv":
            if course.course_dislikes.filter(id=request.user.id).exists():
                course.course_dislikes.remove(request.user)
            if course.course_likes.filter(id=request.user.id).exists():
                course.course_likes.remove(request.user)
                
        data['course_vote'] = render_to_string('home/courses/course_vote.html',{'course':course},request=request)
        return JsonResponse(data)

@login_required      
def course_detail(request, course_university_slug, course_instructor_slug, course_code):
    data = dict()
    course = Course.objects.filter(course_university_slug=course_university_slug,course_instructor_slug=course_instructor_slug,course_code=course_code)\
        .order_by('course_university','course_instructor_slug','course_code','course_year').distinct('course_university','course_instructor_slug','course_code').first()
    taken = request.user.courses.filter(course_university_slug=course_university_slug,course_code=course_code,course_instructor_slug=course_instructor_slug).exists()
    
    if request.method == 'POST':
        form = ReviewForm(request.POST or None)
        if form.is_valid():
            review = form.save(False)
            review.author = request.user
            review.save()
            course.course_reviews.add(review)
        data['reviews_count'] = course.reviews_count()
        data['reviews_all_count'] = course.reviews_all_count()
        data['review'] = render_to_string('home/courses/new_review.html',{'review': review, 'course':course},request=request)
        return JsonResponse(data)
    else:
        form = ReviewForm
    
    sb = request.GET.get('sb','latest')
    o = request.GET.get('rw', 'ins')
    if o == 'all':
        reviews_list = course.get_reviews_all()
    else:
        reviews_list = course.get_reviews(order=sb)

    if o == 'all':
        review_a='active'
        review_s=''
        aria_rea='true'
        aria_res='false'
        link_get=True
    else:
        review_a=''
        review_s='active'
        link_get=False
        aria_res='true'
        aria_rea='false'
           
    page = request.GET.get('page', 1)
    paginator = Paginator(reviews_list , 7)
    try:
        reviews = paginator.page(page)
    except PageNotAnInteger:
        reviews = paginator.page(1)
    except EmptyPage:
        reviews = paginator.page(paginator.num_pages)
    
    reviews_count = course.reviews_count()
    reviews_all_count = course.reviews_all_count()
   
    
    context = {
        'course':course,
        'reviews_count':reviews_count,
        'reviews_all_count':reviews_all_count,
        'reviews':reviews,
        'taken':taken,
        'form':form,
        'course_detail':True,
        'review_a':review_a,
        'review_s':review_s,
        'link_get':link_get,
        'aria_res': aria_res,
        'aria_rea': aria_rea,
    }
    
    return render(request,'home/courses/course_detail.html', context)  


@login_required
def course_share(request,hid):
    data = dict()
    id = hashids.decode(hid)[0]
    course = get_object_or_404(Course, id=id)
    if request.method == 'POST':
        title = "Started taking a new course!"
        content = "Hey! I am taking " + course.course_code + " with professor " + course.course_instructor_fn + " " + course.course_instructor_fn + "!"
        author = request.user
        post = Post(title=title,content=content,author=author)
        post.save()
        
    data['html'] = render_to_string('home/courses/course_shared.html',{'course':course},request=request)
    return JsonResponse(data)

@login_required
def course_instructors(request,course_university_slug,course_code):
    courses = Course.objects.filter(course_university_slug=course_university_slug,course_code=course_code).order_by('course_university_slug','course_instructor_slug','course_code').distinct('course_university_slug','course_instructor_slug','course_code')
    taken = request.user.courses.filter(course_university_slug=course_university_slug,course_code=course_code).exists()
    context = {
        'code':course_code,
        'university': courses.first().course_university,
        'courses': courses,
        'taken':taken
    }
    
    return render(request,'home/courses/course_instructors.html', context)
    
@login_required
def review_like(request, hid, hidc, status):
    
    data = dict()
    
    id1 = hashids.decode(hid)[0]
    id2 =  hashids.decode(hidc)[0]
    
    review = get_object_or_404(Review, id=id1)
    course = get_object_or_404(Course, id=id2)
    
    user = request.user
    if request.method == "POST":
        if status=="like":
            
            """ Send a notification to the review author that someone has disliked their review
                The identity of the user who performed the action (actor) will not be disclosed """
            if review.author != user:    
                message = "CON_CRRW" + "A student liked your review on " # in template course.code should be added in order to add link to page
                description = review.body
                notify.send(sender=user, recipient=review.author, verb=message, description=description, target=course, action_object=review)
            
            review.dislikes.remove(user)
            review.likes.add(user)

        elif status=="dislike":
            
            """ Send a notification to the review author that someone has disliked their review
                The identity of the user who performed the action (actor) will not be disclosed """
            if review.author != user: 
                message = "CON_CRRW" + "A student disliked your review on " # in template course.code should be added in order to add link to page
                description = review.body
                notify.send(sender=user, recipient=review.author, verb=message, description=description, target=course, action_object=review)
            
            review.likes.remove(user)
            review.dislikes.add(user)
            
        elif status=="rmvlike":
            review.likes.remove(user)
            
        elif status == "rmvdislike":
            review.dislikes.remove(user)
            
        elif status == "ulike":
            review.dislikes.remove(user)
            review.likes.add(user)
            if review.author != user:    
                message = "CON_CRRW" + "A student liked your review on " # in template course.code should be added in order to add link to page
                description = review.body
                notify.send(sender=user, recipient=review.author, verb=message, description=description, target=course, action_object=review)
            
        elif status == "udislike":
            review.likes.remove(user)
            review.dislikes.add(user)
            if review.author != user: 
                message = "CON_CRRW" + "A student disliked your review on " # in template course.code should be added in order to add link to page
                description = review.body
                notify.send(sender=user, recipient=review.author, verb=message, description=description, target=course, action_object=review)
            
    data['review'] = render_to_string('home/courses/review_like.html',{'review':review, 'course':course},request=request)
    return JsonResponse(data)

@login_required
def review_delete(request, hidc, hid):
    
    data = dict()
    
    id1 = hashids.decode(hid)[0]
    id2 =  hashids.decode(hidc)[0]
    
    review = get_object_or_404(Review, id=id1)
    course = get_object_or_404(Course, id=id2)
    
    if request.method == 'POST':
        if review.author == request.user:
            review.delete()
            data['form_is_valid'] = True
            data['reviews_count'] = course.reviews_count()
            data['reviews_all_count'] = course.reviews_all_count()
    else:
        context = {'review':review,'course':course}
        data['html_form'] = render_to_string('home/courses/review_delete.html',context,request=request)
    return JsonResponse(data)

@login_required
def university_detail(request):
    
    blockers_id = request.session.get('blockers')
    user_list = []
    uni = request.GET.get('u',request.user.university)
    obj = request.GET.get('obj','std')
    u_empty = ''
    
    data = get_uni_info(uni) 
      
    if data == None:
        data = []
          
    user_list = Profile.objects.filter(Q(university__iexact=uni)|Q(courses__course_university__iexact=uni)).exclude(id__in=blockers_id).order_by('username','last_name').distinct('username')
    cr = Course.objects.filter(course_university__iexact=uni).\
        order_by('course_code','course_instructor','course_instructor_fn').distinct('course_code','course_instructor','course_instructor_fn')
        
    num_courses = cr.count()
    num_enrolled = len(user_list)
    
    if obj == 'std':
        if len(user_list) < 1:
            u_empty='No students found'
          
        page = request.GET.get('page', 1)
        paginator = Paginator(user_list , 7)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
            
        context = {
            'uni':uni,
            'users':users,
            'sa':'-active',
            'u_empty':u_empty,
            'data':data,
            'num_enrolled':num_enrolled,
            'num_courses':num_courses,
            } 
        return render(request,'home/courses/university_detail_students.html',context)
    
    elif obj == 'crs':
        course_list = Course.objects.filter(course_university__iexact=uni).order_by('course_code','course_instructor','course_instructor_fn', 'course_university').distinct('course_code','course_instructor','course_instructor_fn','course_university')
        if course_list.count() < 1:
            u_empty='No courses found'
            
        page = request.GET.get('page', 1)
        paginator = Paginator(course_list , 7)
        try:
            courses = paginator.page(page)
        except PageNotAnInteger:
            courses = paginator.page(1)
        except EmptyPage:
            courses = paginator.page(paginator.num_pages)
         
        context = {
            'uni':uni,
            'courses':courses,
            'ca':'-active',
            'u_empty':u_empty,
            'data':data,
            'num_enrolled':num_enrolled,
            'num_courses':num_courses
            } 
        return render(request,'home/courses/university_detail_courses.html',context)
    
    elif obj == 'ins':
        qs = Course.objects.filter(course_university__iexact=uni).order_by('course_instructor','course_instructor_fn','course_university').distinct('course_instructor','course_instructor_fn','course_university')

        instructor_list = Course.objects.filter(course_university__iexact=uni).annotate(user_count=Count('profiles')).\
            order_by('-user_count').filter(id__in=qs).values_list('course_university','course_instructor','course_instructor_fn','user_count','course_university_slug','course_instructor_slug')
            
        if instructor_list.count() < 1:
            u_empty='No instructors found'
            
        page = request.GET.get('page', 1)
        paginator = Paginator(instructor_list , 7)
        try:
            instructors = paginator.page(page)
        except PageNotAnInteger:
            instructors = paginator.page(1)
        except EmptyPage:
            instructors = paginator.page(paginator.num_pages)
        
        context = {
            'uni':uni,
            'instructors':instructors,
            'ia':'-active',
            'u_empty':u_empty,
            'data':data,
            'num_enrolled':num_enrolled,
            'num_courses':num_courses
            }
        return render(request,'home/courses/university_detail_instructors.html',context)
    
    else:
        return render(request,'home/courses/university_detail.html',{'is_empty':True})

""" Method to show users that user may interact with based specifically on users courses and university + instructors
    Method to be executed and result to cached - receive query set from cache - method constructed on daily basis """    
         
@login_required
def find_students(request):  

    crs_active = prgm_active = ''
    student_list = students = None
    needs_uni_edit = needs_puni_edit = False
    
    sl = request.GET.get('sl', None)

    if sl == 'crs':
        course_codes = request.user.courses.order_by('course_code','course_university','course_instructor','course_instructor_fn','course_year')\
            .distinct('course_code','course_university','course_instructor','course_instructor_fn','course_year').values_list('course_code')
        crs_active='-active'
        if request.user.university != '':
            student_list = Course.objects.same_courses(user=request.user,course_list=course_codes,university=request.user.university)
        else:
            needs_uni_edit=True
    elif sl == 'prgm':
        if request.user.university != '' and request.user.program !='':
            student_list = Profile.objects.same_program(user=request.user,program=request.user.program,university=request.user.university)
        else:
            needs_puni_edit=True
        prgm_active='-active'
    
    if student_list:
        page = request.GET.get('page', 1)
        paginator = Paginator(student_list, 7)
        try:
            students = paginator.page(page)
        except PageNotAnInteger:
            students = paginator.page(1)
        except EmptyPage:
            students = paginator.page(paginator.num_pages)
        
    context = {
        'students':students,
        'sl':sl,
        'prgm_active':prgm_active,
        'crs_active':crs_active,
        'needs_uni_edit':needs_uni_edit,
        'needs_puni_edit':needs_puni_edit
    }
    
    return render(request,'home/courses/related_students/student_list.html',context)
    
@login_required
def get_course_mutual_students(request):
    
    blockers_id = request.session.get('blockers')
    
    hid = request.GET.get('id',None)
    obj = request.GET.get('o','all')
    id = hashids.decode(hid)[0]
    
    course = get_object_or_404(Course, id=id)
    
    if obj == 'ins':
        student_list = Profile.objects.get_students(user=request.user, code=course.course_code, instructor=course.course_instructor, instructor_fn=course.course_instructor_fn, university=course.course_university)
    elif obj == 'all':
        student_list = Profile.objects.filter(courses__course_code=course.course_code,courses__course_university=course.course_university).order_by('last_name','first_name','university').distinct('last_name','first_name','university')

    page = request.GET.get('page', 1)
    paginator = Paginator(student_list, 7)
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        students = paginator.page(1)
    except EmptyPage:
        students = paginator.page(paginator.num_pages)
        
    context = {
        'students':students,
        'course':course,
        'o':obj
    }
    
    return render(request,'home/courses/student_list.html',context)
    
@login_required
def course_list_manager(request):
    
    lists = request.user.course_lists.order_by('created_on')
    
    context = {
        'lists':lists
    }
    return render(request,'home/courses/course_lists/main_menu.html',context)

@login_required
def course_list_create(request):
    
    data = dict()
    
    if request.method == 'POST':
        
        form = CourseListForm(request.POST)
        if form.is_valid():  
            li = form.save(False)
            li.creator = request.user
            li.save()
            data['form_is_valid'] = True
            data['list'] = render_to_string('home/courses/course_lists/list_obj.html',{'list':li},request=request)
        else:
            data['form_is_valid'] = False
    else:
        form = CourseListForm      
    context = {
    'form':form,
	}
    
    data['html_form'] = render_to_string('home/courses/course_lists/list_create_form.html',context,request=request)
    return JsonResponse(data)

@login_required
def course_list_edit(request, hid):
    
    data = dict()
    fc = ''
    
    id = hashid_list.decode(hid)[0]
    li = get_object_or_404(CourseList, id=id)

    if request.method == 'POST':
        form = CourseListForm(request.POST,instance=li)
        if form.is_valid():  
            li = form.save(False)
            li.creator = request.user
            li.save()
            data['form_edit_is_valid'] = True
            data['new_url'] = reverse('home:course-list-obj',kwargs={'hid':li.get_hashid()})
            data['list'] = render_to_string('home/courses/course_lists/list_obj.html',{'list':li},request=request)
        else:
            data['form_is_valid'] = False
    else:
        form = CourseListForm(instance=li)
        form.instance.creator = request.user
        
    a=request.GET.get('a',None)
    if a == 're':
        fc = 'form-redirect-go'
        
    context = {
    'form':form,
    'list':li,
    'fc':fc
    }
    
    data['html_form'] = render_to_string('home/courses/course_lists/list_edit_form.html',context,request=request)
    return JsonResponse(data)

@login_required
def course_list_delete(request, hid):
    
    data = dict()
    id = hashid_list.decode(hid)[0]
    li = get_object_or_404(CourseList, id=id)
    
    if request.method == 'POST':
        if li.creator == request.user:
            li.delete()
            data['form_delete_is_valid'] = True
            a = request.POST.get('ac',None)
            if a == 'h':
                data['new_url'] = reverse('home:course-list-manager')
                data['redirect'] = True
    else:
        a = request.GET.get('a', None)
        context = {'list':li, 'a':a }
        data['html_form'] = render_to_string('home/courses/course_lists/list_delete_form.html',context,request=request)
    return JsonResponse(data)

@login_required
def course_list_obj(request, hid):
    
    id = hashid_list.decode(hid)[0]
    li = get_object_or_404(CourseList, id=id)
    
    
    num_items = li.added_courses.count()
    
    o = request.GET.get('ol', 'co')
    if o:
        order = {'co':'-created_on', 'cu':'course_university','ci':'course_instructor','cc':'course_code'}
        objects = li.added_courses.order_by(order[o])
    else:
        objects = li.added_courses.order_by('created_on')
    
    context = {
        'list':li,
        'courses':objects,
        'num_items': num_items,
        o+'_selected':'selected'
    }
    return render(request,'home/courses/course_lists/course_list.html',context)

@login_required
def course_list_obj_add_course(request, hid):
    
    id = hashid_list.decode(hid)[0]
    li = get_object_or_404(CourseList, id=id)
    
    data = dict()
    
    if request.method == 'POST':
        form = CourseListObjectsForm(request.POST)
        if form.is_valid(): 
            cr = form.save(False)
            cr.parent_list = li
            cr.author = request.user
            cr.save()
            data['form_crsaction_is_valid'] = True
            data['new_url'] = reverse('home:course-list-obj',kwargs={'hid':li.get_hashid()})
        else:
            data['form_is_valid'] = False
    else:
        form = CourseListObjectsForm
    
    action_url = reverse('home:course-list-addcrs',kwargs={'hid':li.get_hashid()})
    context = {
    'form':form,
    'list':li,
    'title_m':'Add Course',
    'actionbtn_m':'Add',
    'form_class':'crs-itm-',
    "action_url":action_url
	}
    
    data['html_form'] = render_to_string('home/courses/course_lists/list_create_form.html',context,request=request)
    return JsonResponse(data)

@login_required
def course_list_obj_remove_course(request, hid, hid_item):
    
    data=dict()
    
    id = hashid_list.decode(hid)[0]
    id2 = hashids.decode(hid_item)[0]
    li = get_object_or_404(CourseList, id=id)
    crs = get_object_or_404(CourseListObjects, id=id2)
    
    if request.method == 'POST':
        if li.creator == request.user and crs.author == request.user:
            crs.delete()
            data['form_crsaction_is_valid'] = True
            data['new_url'] = reverse('home:course-list-obj',kwargs={'hid':li.get_hashid()})    
    else:
        action_url = reverse('home:course-list-deletecrs',kwargs={'hid':li.get_hashid(),'hid_item':crs.get_hashid()})
        context = {
        'list':li, 
        'crs':crs,
        'delete_text':"Are you sure you want to permanently remove this item from your list?",
        'form_class':'crs-itm-',
        'action_url':action_url,
         }
        data['html_form'] = render_to_string('home/courses/course_lists/list_delete_form.html',context,request=request)
    return JsonResponse(data)

@login_required
def course_list_obj_edit_course(request, hid, hid_item):
    
    data=dict()
    
    id = hashid_list.decode(hid)[0]
    id2 = hashids.decode(hid_item)[0]
    li = get_object_or_404(CourseList, id=id)
    crs = get_object_or_404(CourseListObjects, id=id2)
    
    if request.method == 'POST':
        form = CourseListObjectsForm(request.POST,instance=crs)
        if li.creator == request.user and crs.author == request.user:
            crs = form.save(False)
            crs.parent_list = li
            crs.author = request.user
            crs.save()
            data['form_crsaction_is_valid'] = True
            data['new_url'] = reverse('home:course-list-obj',kwargs={'hid':li.get_hashid()})    
    else:
        form = CourseListObjectsForm(instance=crs)
        action_url = reverse('home:course-list-editcrs',kwargs={'hid':li.get_hashid(),'hid_item':crs.get_hashid()})
        context = {
        'form':form,
        'list':li, 
        'crs':crs,
        'form_class':'crs-itm-',
        'action_url':action_url,
         }
        data['html_form'] = render_to_string('home/courses/course_lists/list_edit_form.html',context,request=request)
    return JsonResponse(data)
    
@login_required
def course_save(request,id):
    
    data = dict()
    course = get_object_or_404(Course,id=id)
    if request.method == "POST":
        if request.user.saved_courses.filter(course_instructor=course.course_instructor,course_university=course.course_university,course_code=course.course_code).exists():
            data['message'] = "You have already saved this course"
        else:
            request.user.saved_courses.add(course)
            data['message'] = course.course_code + " with professor " + course.course_instructor + " has been successfully added to your saved courses"
        return JsonResponse(data)
    
@login_required
def remove_saved_course(request,hid):
    
    data = dict()
    id =  hashids.decode(hid)[0]
    course = get_object_or_404(Course, id=id)
    if request.method == "POST":
        request.user.saved_courses.remove(course)
    else:
        context = {
            'course':course,
        }
        data['html_form'] = render_to_string('home/courses/saved-course-remove.html',context,request=request)
    return JsonResponse(data)
        
        
@login_required
def saved_courses(request):
    courses = request.user.saved_courses.all()
    return render(request,'home/courses/user_saved_courses.html',{'courses':courses})


@login_required
def blog(request):
    
    blogs_list = Blog.objects.get_blogs(user=request.user)
    
    page = request.GET.get('page', 1)
    paginator = Paginator(blogs_list, 10)
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)
    context = {
        'blogs':blogs,
        }
    
    return render(request, 'home/blog/blog.html', context)

def blog_create(request):
    
    if request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():
             blog = form.save(False)
             blog.author = request.user
             blog.save()
             form.save_m2m()
             return redirect('home:blog-detail',hid=blog.guid_url, t=blog.slug)
    else:
        form = BlogForm
    context = {
        'form':form,
    }
    return render(request,'home/blog/blog_create.html', context)

def blog_detail(request, hid, t):
    
    blog = get_object_or_404(Blog, guid_url=hid, slug=t)
    replies_count = blog.blog_replies.count()
    context = {'blog':blog,'replies_count':replies_count}
    return render(request,'home/blog/blog_detail.html',context)

@login_required
def blog_update(request, hid, t):
    
    data = dict()
    blog = get_object_or_404(Blog, guid_url=hid, slug=t)
    if blog.author == request.user:
        if request.method == 'POST':
            form = BlogForm(request.POST,instance=blog)
            form.instance.author = request.user
            if form.is_valid():
                form.save()
                return redirect('home:blog-detail',hid=blog.guid_url, t=blog.slug) 
        else:
            form = BlogForm(instance=blog)
            form.instance.author = request.user
            is_edit = True
            context = {
                'form':form,
                'blog':blog,
                'is_edit':is_edit,
            }
        return render(request,'home/blog/blog_create.html', context)

@login_required
def blog_delete(request, hid, t):
    
    data = dict()
    blog = get_object_or_404(Blog, guid_url=hid, slug=t)
    if request.method == 'POST':
        if blog.author == request.user:
            blog.delete()
            data['form_is_valid'] = True
    else:
        context = {'blog':blog}
        data['html_form'] = render_to_string('home/blog/blog_delete.html',context,request=request)
    return JsonResponse(data)
        
@login_required
def blog_like(request,guid_url):
    
    data = dict()
    blog = get_object_or_404(Blog, guid_url=guid_url)
    user = request.user
    if request.method == 'POST':   
        if blog.likes.filter(id=user.id).exists():
            blog.likes.remove(user)
        else:
            blog.likes.add(user)
            if blog.author.get_notify and blog.author.get_blog_notify_all and blog.author.get_blog_notify_likes:
                message = "CON_BLOG" + "liked your blog post." 
                notify.send(sender=user, recipient=blog.author, verb=message, target=blog)
        data['blog_likes'] = render_to_string('home/blog/blog_like.html',{'blog':blog},request=request)
        return JsonResponse(data)

@login_required
def blog_replies(request,guid_url,slug):
    
    data = dict()
    blog = get_object_or_404(Blog, guid_url=guid_url,slug=slug)
    replies_list = blog.blog_replies.order_by('-date_replied')
    
    page = request.GET.get('page', 1)
    paginator = Paginator(replies_list, 10)
    try:
        replies = paginator.page(page)
    except PageNotAnInteger:
        replies = paginator.page(1)
    except EmptyPage:
        replies = paginator.page(paginator.num_pages)
        
    replies_count = blog.blog_replies.count()
    user=request.user
    if request.method == 'POST':   
        form = BlogReplyForm(request.POST or None)
        if form.is_valid():
            reply = form.save(False)
            reply.author = request.user
            reply.blog  = blog
            reply.save()
            if user != blog.author:
                if blog.author.get_notify and blog.author.get_blog_notify_all and blog.author.get_blog_notify_comments:
                    message = "CON_BLOG" + "replied to your blog post." 
                    description = reply.content
                    notify.send(sender=user, recipient=blog.author, description=description, verb=message, target=blog)
            data['form_is_valid'] = True
            data['new_reply'] = render_to_string('home/blog/blog_reply_new.html',{'reply':reply,'blog':blog},request=request)
            data['reply_count'] = num_format(blog.blog_replies.count())
            return JsonResponse(data)
    else: 
        form = BlogReplyForm
    context = {'blog':blog,
                'form':form,
                'replies':replies,
                'replies_count':replies_count,
                }
    
    return render(request,'home/blog/blog_replies.html',context)

@login_required
def blog_reply_like(request,hid):
    
    data = dict()
    id = hashids.decode(hid)[0]
    reply = get_object_or_404(BlogReply, id=id)
    user = request.user
    if request.method == 'POST':   
        if reply.reply_likes.filter(id=user.id).exists():
            reply.reply_likes.remove(user)
        else:
            reply.reply_likes.add(user)
            if user != reply.author:
                if reply.author.get_notify and reply.author.get_blog_notify_all and reply.author.get_blog_notify_comments:
                    message = "CON_BLOG" + "liked your reply." 
                    description = reply.content
                    notify.send(sender=user, recipient=reply.author, description=description, verb=message, target=blog)
        data['reply_likes'] = render_to_string('home/blog/blog_reply_like.html',{'reply':reply},request=request)
        return JsonResponse(data)
    
@login_required
def blog_reply_delete(request,hid, guid_url):
    
    data = dict()
    id = hashids.decode(hid)[0]
    reply = get_object_or_404(BlogReply, id=id)
    blog = get_object_or_404(Blog, guid_url=guid_url)
    
    if request.method == 'POST':
        if request.user == blog.author or request.user == reply.author:
            reply.delete()
            data['form_is_valid'] = True
            data['reply_count'] = num_format(blog.blog_replies.count())
    else:
        context = {'blog':blog,'reply':reply}
        data['html_form'] = render_to_string('home/blog/blog_reply_delete.html',context,request=request)
    return JsonResponse(data)

@login_required
def blog_reply_edit(request,hid, guid_url, slug):
    
    data = dict()
    id = hashids.decode(hid)[0]
    reply = get_object_or_404(BlogReply, id=id)
    blog = get_object_or_404(Blog, guid_url=guid_url, slug=slug)
    
    if request.method == 'POST':
        if request.user == blog.author or request.user == reply.author:
            form = BlogReplyForm(request.POST,instance=reply)
            form.instance.author = request.user
            if form.is_valid():
                form.save()
                return redirect('home:blog-replies',guid_url=blog.guid_url, slug=blog.slug) 
    else:
        form = BlogReplyForm(instance=reply)
        context = {
            'form':form,
            'blog':blog,
            'reply':reply
            }
    return render(request,'home/blog/blog_replies_edit.html',context)
    
    
    
@login_required
def tags_post(request, slug):
    
    tag = get_object_or_404(Tag, slug=slug)
    blockers_id = request.session.get('blockers')
    
    posts_list = Post.objects.select_related("author").exclude(author__id__in=blockers_id).filter(tags=tag).order_by('-last_edited')
    related_tags = Post.tags.most_common(extra_filters={'post__in': posts_list })[:5]
    num_obj = posts_list.count()
    if num_obj > 1:
        s="posts"   
    else:
        s="post"
    page = request.GET.get('page', 1)
    paginator = Paginator(posts_list, 10)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    is_tag = True
    context = {
        'tag' : tag,
        'posts':posts,
        'is_tag':is_tag,
        'num_obj':num_obj,
        's':s,
        'related_tags':related_tags
        }
    return render(request, 'home/homepage/home.html', context)

@login_required
def tags_blog(request, slug):
    
    tag = get_object_or_404(Tag, slug=slug)
    blockers_id = request.session.get('blockers')
    
    blog_list = Blog.objects.select_related("author").exclude(author__id__in=blockers_id).filter(tags=tag).order_by('-last_edited')
    related_tags = Blog.tags.most_common(extra_filters={'blog__in': blog_list })[:5]
    num_obj = blog_list.count()
    if num_obj > 1:
        s="blogs" 
    else:
        s="blog"
    page = request.GET.get('page', 1)
    paginator = Paginator(blog_list, 10)
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)
    is_tag = True
    context = {
        'tag' : tag,
        'blogs':blogs,
        'is_tag':is_tag,
        'num_obj':num_obj,
        's':s,
        'related_tags':related_tags
        }
    return render(request, 'home/blog/blog.html', context)



@login_required
def search(request):
    if request.method == 'GET':
        search_term = request.GET.get('q', None)
        if not SearchLog.objects.filter(search_text__iexact=search_term).exists():
            search_term = search_term.lower()
            sl = SearchLog.objects.create(search_text=search_term)
            request.user.recent_searches.add(sl)
        elif SearchLog.objects.filter(search_text__iexact=search_term).exists():
            sl = SearchLog.objects.filter(search_text__iexact=search_term).first()
            request.user.recent_searches.add(sl)
            
        o = request.GET.get('o', None)
        if o == 'top':
            
            posts = Post.objects.search_topresult(search_term)
            blogs = Blog.objects.search_topresult(search_term)
            users = Profile.objects.search_topresult(search_term)
            courses = Course.objects.search(search_term)[:3]
            
            related_terms = SearchLog.objects.related_terms(search_term)
            
            if (posts.exists() or blogs.exists() or users.exists() or courses.exists()):
                empty = False 
            else:
                empty = True
                
            context = {
                'posts':posts,
                'blogs':blogs,
                'users':users,
                'empty':empty,
                'related_terms':related_terms,
                'courses':courses,
                'q':search_term,
                'top_active':'-active'
            }
            
            return render(request, 'home/search/search_top.html', context)
        
            
        if o == 'post':
            post_list = Post.objects.search(search_term)
            tags = Post.tags.most_common(extra_filters={'post__in': post_list })[:5]
            page = request.GET.get('page', 1)
            paginator = Paginator(post_list, 10)
            try:
                posts = paginator.page(page)
            except PageNotAnInteger:
                posts = paginator.page(1)
            except EmptyPage:
                posts = paginator.page(paginator.num_pages)
            context = {
                'posts':posts,
                'tags':tags,
                'q':search_term,
                'post_active':'-active'
            }
            return render(request, 'home/search/search_post.html', context)
        
        if o == 'blog':
            blog_list = Blog.objects.search(search_term)
            page = request.GET.get('page', 1)
            paginator = Paginator(blog_list, 10)
            try:
                blogs = paginator.page(page)
            except PageNotAnInteger:
                blogs = paginator.page(1)
            except EmptyPage:
                blogs = paginator.page(paginator.num_pages)
            context = {
                'blogs':blogs,
                'q':search_term,
                'blog_active':'-active'
            }
            return render(request, 'home/search/search_blog.html', context)
        
        
        if o == 'users':
            if len(search_term.split()) > 1:
                users_list = Profile.objects.search_combine(search_term)
            else:
                users_list = Profile.objects.search(search_term)
                
            page = request.GET.get('page', 1)
            paginator = Paginator(users_list, 10)
            try:
                users = paginator.page(page)
            except PageNotAnInteger:
                users = paginator.page(1)
            except EmptyPage:
                users = paginator.page(paginator.num_pages)
            context = {
                'users':users,
                'q':search_term,
                'users_active':'-active'
            }
            return render(request, 'home/search/search_user.html', context)
        
        if o == 'course':
            
            course_list = Course.objects.search(search_term)
                
            page = request.GET.get('page', 1)
            paginator = Paginator(course_list, 7)
            try:
                courses = paginator.page(page)
            except PageNotAnInteger:
                courses = paginator.page(1)
            except EmptyPage:
                courses = paginator.page(paginator.num_pages)
            context = {
                'courses':courses,
                'q':search_term,
                'course_active':'-active'
            }
            return render(request, 'home/search/search_course.html', context)
        
        
    
@login_required
def search_dropdown(request):
    
    if request.method == 'GET':
        search_term = request.GET.get('q', None)
        user_recent_search = [str(i) for i in request.user.recent_searches.order_by('-time_stamp')[:3]]
        most_similar = [str(i) for i in SearchLog.objects.filter(search_text__icontains=search_term).order_by('-time_stamp')[:4]]
        
        data = {
            'search_user': user_recent_search,
            'search_top': most_similar,
        } 

        return JsonResponse(data,safe=False)
    
@login_required
def remove_search(request):
    
    data = dict()
    term = request.GET.get('t',None)
    if request.method == 'POST': 
        if term:
            term = term.lower()
            if request.user.is_authenticated:
                search_object = SearchLog.objects.get(search_text=term)
                request.user.recent_searches.remove(search_object)
                data['indv_search_remove'] = True
                return JsonResponse(data)
        else:
            request.user.recent_searches.clear()
            data['all_search_remove'] = True
            return JsonResponse(data)
    

        
        
        

    