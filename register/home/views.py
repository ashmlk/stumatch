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
from .models import Post, Comment
from .forms import PostForm, CommentForm, CourseForm, ImageForm

@login_required
def home(request):
    posts = Post.objects.all()
    posts = Post.objects.order_by('-last_edited')
    context = { 'posts':posts }
    return render(request, 'home/homepage/home.html', context)
    
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
        form = PostForm(request.POST)
        if form.is_valid():      
            post = form.save(False)
            post.author = request.user
            #post.likes = None
            post.save()
            data['form_is_valid'] = True
            posts = Post.objects.all()
            posts = Post.objects.order_by('-last_edited')
            data['posts'] = render_to_string('home/posts/home_post.html',{'posts':posts},request=request)
        else:
            data['form_is_valid'] = False
    else:
        form = PostForm       
    context = {
    'form':form
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

class PostImageUpload(LoginRequiredMixin, View):
    
    def get(self, request):
        images = Images.objects.all()
        return render(self.request, 'home/posts/post_create.html', {'images':images} ) 
    
    def post(self, request):
        data = dict()
        form = ImageForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            image = form.save(False)
            image.save()
            data = {'is_valid': True, 'name': image.file.name, 'url': image.file.url} 
        else:
            data['is_valid'] = False
        return JsonResponse(data)

    
class PostLikeToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        pk = self.kwargs.get("pk")
        print(slug)
        obj = get_object_or_404(Post, pk=pk)
        url_ = obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated():
            if user in obj.likes.all():
                obj.likes.remove(user)
            else:
                obj.likes.add(user)
        return url_

#Responsible for toggling like button
class PostLikeAPIToggle(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk, format=None):
        # slug = self.kwargs.get("slug")
        obj = get_object_or_404(Post, pk=pk)
        url = obj.get_absolute_url()
        user = self.request.user
        updated = False
        liked = False
        if user.is_authenticated():
            if user in obj.likes.all():
                liked = False
                obj.likes.remove(user)
            else:
                liked = True
                obj.likes.add(user)
            updated = True
        data = {
            "updated": updated,
            "liked": liked
        }
        return Response(data)


# Course views
def course_list(request):
    pass

def course_add(request):
    pass

def course_update(request):
    pass

def course_delete(request):
    pass

