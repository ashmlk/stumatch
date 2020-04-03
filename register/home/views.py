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
    ImageFormset = modelformset_factory(Images,form=ImageForm,extra=4)
    if request.method == 'POST':
        form = PostForm(request.POST)
        formset = ImageFormset(request.POST or None, request.FILES or None)
        if form.is_valid() and formset.is_valid():    
            post = form.save(False)
            post.author = request.user
            #post.likes = None
            post.save()
            for i in formset:
                try:
                    i = Images(post=post, image=f.cleaned_data.get('image'))
                    i.save()
                except Exception as e:  
                    break
            data['form_is_valid'] = True
            posts = Post.objects.all()
            images = Images.objects.all()
            posts = Post.objects.order_by('-last_edited')
            data['posts'] = render_to_string('home/posts/home_post.html',{'posts':posts,'images':images},request=request)
        else:
            data['form_is_valid'] = False
    else:
        form = PostForm  
        formset = ImageFormset(queryset=Images.objects.none())     
    context = {
    'form':form,
    'formset':formset,
	}
    data['html_form'] = render_to_string('home/posts/post_create.html',context,request=request)
    return JsonResponse(data) 


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
def post_delete(request, id):
    data = dict()
    post = get_object_or_404(Post, id=id)
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
def post_detail(request, id):
    data = dict()
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(False)
            comment.post = post
            comment.name = request.user
            comment.save()
            comments = post.comments.all()
            data['form_is_valid'] = True
            data['comments'] = render_to_string('home/posts/post_comment.html', { 'comments':comments, 'post':post }, request=request)
        else:
            data['form_is_valid'] = False
    else: 
        form = CommentForm
        comments = post.comments.all()
    context  = {
        'form': form,
        'comments': comments,
        'post': post
    }
    data['html_data'] = render_to_string('home/posts/post_detail.html', context,request=request)
    return JsonResponse(data)


@login_required
def post_like(request,id):
    data = dict()
    post = get_object_or_404(Post, id=id)
    user = request.user
    if post.likes.filter(id=user.id).exists():
        post.likes.remove(user)
    else:
        post.likes.add(user)
    data['form_is_valid'] = True
    posts = Post.objects.all()
    posts = Post.objects.order_by('-last_edited')
    data['html'] = render_to_string('home/posts/home_post.html',{'posts':posts},request=request)
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

