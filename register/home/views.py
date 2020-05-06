from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
    RedirectView
)
from django.forms import modelformset_factory 
from .models import Post, Comment, Images, Course
from .forms import PostForm, CommentForm, CourseForm, ImageForm
from .post_guid import uuid2slug, slug2uuid
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

MAX_COURSES = 7

@login_required
def home(request):
    posts = Post.objects.all()
    images = Images.objects.all()
    posts = Post.objects.order_by('-last_edited')
    context = { 'posts':posts }
    return render(request, 'home/homepage/home.html', context)

@login_required
def user_posted_home(request):
    posts = Post.objects.filter(author=request.user).order_by('-last_edited')
    images = Images.objects.all()
    context = { 'posts':posts }
    return render(request, 'home/homepage/user_posts.html', context)
    

@login_required
def post_create(request):
    data = dict()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():  
            post = form.save(False)
            post.author = request.user
            post.save()
            if request.FILES is not None:
                added = []
                images = request.FILES.getlist('images[]')
                for i in images:
                    if i not in added:
                        image_instance = Images.objects.create(image=i,post=post)
                        image_instance.save()
                        added.append(i)
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
    comments = Comment.objects.filter(post=post,reply=None)
    if request.method == 'POST':
        form = CommentForm(request.POST or None)
        if form.is_valid():
            comment = form.save(False)
            reply_id = request.POST.get('comment_id')
            comment_qs = None
            if reply_id:
                comment_qs = Comment.objects.get(id=reply_id)
            comment.name = request.user
            comment.post = post
            comment.reply = comment_qs
            comment.save()
        else:
            data['is_valid'] = False
    else:
        form = CommentForm()
    guid_url = post.guid_url
    comment_count = post.comment_count()
    context = {'post':post,
                'form':form,
                'comments':comments,
                'comment_count':comment_count,
                'guid_url':guid_url,
                }
    if request.is_ajax():
        comments_new = Comment.objects.filter(post=post,reply=None)
        comment_count_new = post.comment_count()
        context_new = {'post':post,
                        'comments':comments_new,
                        'comment_count':comment_count_new,
                        'guid_url':guid_url,
                        'form':form,
                    }
        data['comments'] = render_to_string('home/posts/post_comment.html',context_new,request=request)
        data['likes'] = render_to_string('home/posts/likes.html',context_new,request=request)
        return JsonResponse(data)
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
        data['post_likes'] = render_to_string('home/posts/likes.html',{'post':post},request=request)
        return JsonResponse(data)
        

@login_required
def comment_like(request,guid_url,id):
    data = dict()
    guid_url = guid_url
    comment = get_object_or_404(Comment, id=id)
    user = request.user
    if request.method == 'POST':    
        if comment.likes.filter(id=user.id).exists():
            comment.likes.remove(user)
        else:
            comment.likes.add(user)
        data['comment'] = render_to_string('home/posts/comment_like.html',{'comment':comment,'guid_url':guid_url},request=request)
        return JsonResponse(data)


@login_required
def post_like_list(request, guid_url):
    data = dict()
    post = get_object_or_404(Post, guid_url=guid_url)
    post_likes = post.likes.all()
    data['html'] = render_to_string('home/posts/post_like_list.html',{'post_likes':post_likes},request=request)
    return JsonResponse(data)

@login_required
def post_comment_list(request, guid_url):
    data = dict()
    post = get_object_or_404(Post, guid_url=guid_url)
    post_comments = Comment.objects.filter(post=post,reply=None)
    data['html'] = render_to_string('home/posts/post_comment_list.html',{'post_comments':post_comments},request=request)
    return JsonResponse(data)

# Course views
@login_required
def courses(request):
    courses = request.user.courses.all()
    courses = courses.order_by("course_code")
    context = { 'courses':courses }
    return render(request,'home/courses/course_list.html',context)

@login_required
def courses_instructor(request,par1,par2):
    courses = Course.objects.filter(course_instructor=par2,course_university=par1)
    instructor=par2
    university=par1
    university = university.lower()
    university = university.replace('university','')
    context = {
         'courses':courses,
         'instructor':instructor,
         'university':university,
         }
    return render(request,'home/courses/instructor_course_list.html',context)

@login_required
def course_add(request):
    if request.method == "POST":
        form = CourseForm(request.POST or none)
        if form.is_valid():
            course = form.save(False)
            code = course.course_code.upper().replace(' ', '')
            uni = course.course_university.strip().lower()
            ins = course.course_instructor.strip().lower()
            has_coursed = request.user.courses.filter(course_code=code,course_instructor=ins,course_year=course.course_year,course_university=uni,course_semester=course.course_semester).exists()
            max_reached =  request.user.courses.filter(course_year=course.course_year,course_university=uni,course_semester=course.course_semester).count()
            course_exists = Course.objects.filter(course_code=code,course_instructor=ins,course_year=course.course_year,course_university=uni,course_semester=course.course_semester,course_difficulty=course.course_difficulty).exists()
            if max_reached > 7:
                form = CourseForm
                message = "You have reached maximum number of courses per semester for the " + course.sem + " semester in "+ course.course_year 
                context = {
                    'form':form,
                    'message': message,
                }
                return render(request,'home/courses/course_add.html', context)  
            elif has_coursed:
                form = CourseForm
                message = "It's seems you have already added this course. Please try again."
                context = {
                    'form':form,
                    'message': message,
                }
                return render(request,'home/courses/course_add.html', context)
            else:
                if course_exists:
                    c = Courses.objects.filter(course_code=code,course_instructor=ins,course_year=course.course_year,course_university=uni,course_semester=course.course_semester,course_difficulty=course.course_difficulty)
                    request.user.courses.add(c)
                else:
                    course.save()
                    request.user.courses.add(course)
                return redirect('home:courses')
    else:
        form = CourseForm
    context = {
        'form':form,
    }
    return render(request,'home/courses/course_add.html', context)
        

def course_update(request):
    pass

def course_remove(request, id):
    data= dict()
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

def course_vote(request, id, code, status=None):
    data = dict()
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
            

