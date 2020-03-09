from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.template.loader import render_to_string
from django.http import JsonResponse

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
from .forms import PostForm, CommentForm, CourseForm

# Create your views here.
@login_required
def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'home/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'home/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']  

@login_required    
def post_detail(request, id):
    template_name = 'post_detail.html'
    post = get_object_or_404(Post, id=id)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, 'post_detail.html', {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})
    
    
class PostCreateView(LoginRequiredMixin, CreateView):
    login_url='main:user_login'
    permission_denied_message = "Please login before continuing"
    model = Post
    fields = ['title', 'content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
@login_required
def save_all(request,form,template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():      
            form.save()
            data['form_is_valid'] = True
            posts = Post.objects.all()
            data['posts'] = render_to_string('home/home_post.html',{'posts':posts})
        else:
            data['form_is_valid'] = False
    context = {
    'form':form
	}
    data['html_form'] = render_to_string(template_name,context,request=request)
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
    return save_all(request, form, 'home/post_update.html')

@login_required
def post_delete(request, id):
    data = dict()
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        post.delete()
        data['form_is_valid'] = True
        posts = Post.objects.all()
        data['posts'] = render_to_string('home/home_post.html',{'posts':posts})
    else:
        context = {'post':post}
        data['html_form'] = render_to_string('home/post_delete.html',context,request=request)

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
