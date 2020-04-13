from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.template.loader import render_to_string
from django.http import JsonResponse
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
from .models import Post, Comment, Images
from .forms import PostForm, CommentForm, CourseForm, ImageForm
from .post_guid import uuid2slug, slug2uuid
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

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
def save_all(request,form,template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():      
            form.save()
            data['form_is_valid'] = True
            posts = Post.objects.all()
            posts = Post.objects.order_by('-last_edited')
            data['posts'] = render_to_string('home/posts/home_post.html',{'posts':posts},request=request)
        else:
            data['form_is_valid'] = False
            
    context = {
    'form':form
	}
    data['html_form'] = render_to_string(template_name,context,request=request)
    return JsonResponse(data) 

@login_required
def post_create(request):
    data = dict()
    if request.method == 'POST':
        image_form = ImageForm(request.POST or None, request.FILES or None)
        form = PostForm(request.POST)
        if form.is_valid() and image_form.is_valid():  
            post = form.save(False)
            post.author = request.user
            post.save()
            images = request.FILES.getlist('image')
            for i in images:
                image_instance = Images(file=i,post=post)
                image_instance.save()
            data['form_is_valid'] = True
            posts = Post.objects.all()
            posts = Post.objects.order_by('-last_edited')
            data['posts'] = render_to_string('home/posts/home_post.html',{'posts':posts},request=request)
        else:
            data['form_is_valid'] = False
    else:
        image_form = ImageForm
        form = PostForm      
    context = {
    'form':form,
    'image_form':image_form
	}
    data['html_form'] = render_to_string('home/posts/post_create.html',context,request=request)
    return JsonResponse(data) 

# Do Not Change
@login_required
def post_update(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        form = PostForm(request.POST,instance=post)
        form.instance.author = request.user
    else:
        form = PostForm(instance=post)
        form.instance.author = request.user
    return save_all(request, form, 'home/posts/post_update.html')

@login_required
def post_delete(request, guid_url):
    data = dict()
    post = get_object_or_404(Post, guid_url=guid_url)
    if request.method == 'POST':
        post.delete()
        data['form_is_valid'] = True
        posts = Post.objects.all()
        posts = Post.objects.order_by('-last_edited')
        data['posts'] = render_to_string('home/posts/home_post.html',{'posts':posts},request=request)
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
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(False)
            reply_id = request.POST.get('comment_id')
            comment_qs = None
            if reply_id:
                comment_qs = Comment.objects.get(id=reply_id)
            comment.name = request.user
            comment.post = post
            comment.reply=comment_qs
            comment.save()
        else:
            data['is_valid'] = False
    else:
        form = CommentForm
    comment_count = post.comments.count()
    context = {'post':post,
                'form':form,
                'comments':comments,
                'comment_count':comment_count,
                }
    if request.is_ajax():
        data['comments'] = render_to_string('home/posts/post_comment.html',{'comments':comments,'comment_count':comment_count},request=request)
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
        posts = Post.objects.all()
        posts = Post.objects.order_by('-last_edited')
        data['posts'] = render_to_string('home/posts/home_post.html',{'posts':posts},request=request)
        data['posts-detail'] = render_to_string('home/posts/home_post.html',{'posts':posts},request=request)
        return JsonResponse(data)

# Course views
def course_list(request):
    pass

def course_add(request):
    pass

def course_update(request):
    pass

def course_delete(request):
    pass

