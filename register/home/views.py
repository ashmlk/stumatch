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
from django.utils import timezone
from django.db.models import Q
from django.db.models import Max, Min
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
from .models import Post, Comment, Images, Course, Review
from main.models import Profile
from .forms import PostForm, CommentForm, CourseForm, ImageForm, ReviewForm
from .post_guid import uuid2slug, slug2uuid
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import datetime


MAX_COURSES = 7

@login_required
def home(request):
    posts = Post.objects.all()
    images = Images.objects.all()
    posts = Post.objects.order_by('-last_edited')
    context = { 'posts':posts }
    return render(request, 'home/homepage/home.html', context)

@login_required
def users_posts(request,username):
    u = get_object_or_404(Profile,username=username)
    posts = Post.objects.filter(author=request.user).order_by('-last_edited')
    context = { 'posts':posts }
    return render(request, 'home/homepage/home.html', context)

@login_required
def latest_posts(request):
    now = datetime.datetime.now(tz=timezone.utc)
    t_24 = now - datetime.timedelta(hours=24)
    posts = Post.objects.filter(last_edited__range=(t_24,now))
    context = { 'posts':posts,'latest':True }
    return render(request, 'home/homepage/home.html', context)
   
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
def comment_delete(request,id):
    data=dict()
    comment=get_object_or_404(Comment,id=id)
    if request.method=="POST":
        if comment.name==request.user:
            comment.delete()
            data['form_is_valid'] = True
    else:
        context = {'comment':comment}
        data['html_form'] = render_to_string('home/posts/comment_delete.html',context,request=request)
    return JsonResponse(data)
            
# Method for returning a list of all users who liked a post   
@login_required
def post_like_list(request, guid_url):
    data = dict()
    post = get_object_or_404(Post, guid_url=guid_url)
    post_likes = post.likes.all()
    data['html'] = render_to_string('home/posts/post_like_list.html',{'post_likes':post_likes},request=request)
    return JsonResponse(data)

# Method for returning a list of all users who commented on a post 
@login_required
def post_comment_list(request, guid_url):
    data = dict()
    post = get_object_or_404(Post, guid_url=guid_url)
    post_comments = Comment.objects.filter(post=post,reply=None)
    data['html'] = render_to_string('home/posts/post_comment_list.html',{'post_comments':post_comments},request=request)
    return JsonResponse(data)

'''
Below is all views related to course section
All methods are for course section exclusively
'''
@login_required
def courses(request):
    courses = request.user.courses.all()
    courses = courses.order_by("course_code")
    context = { 'courses':courses }
    return render(request,'home/courses/course_list.html',context)

@login_required
def courses_instructor(request,par1,par2):
    courses = Course.objects.filter(course_instructor_slug=par2,course_university_slug=par1).order_by('course_code','course_instructor_slug','course_university_slug').distinct('course_code','course_instructor_slug','course_university_slug')
    context = {
         'courses':courses,
         'instructor':courses.first().course_instructor,
         'university':courses.first().course_university,
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
                    c = Courses.objects.get(course_code=code,course_instructor=ins,course_year=course.course_year,course_university=uni,course_semester=course.course_semester,course_difficulty=course.course_difficulty)
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
            
def course_detail(request, course_university_slug, course_instructor_slug, course_code):
    data = dict()
    course = Course.objects.filter(course_university_slug=course_university_slug,course_instructor_slug=course_instructor_slug,course_code=course_code).order_by('course_university','course_instructor','course_code','course_year').distinct('course_university','course_instructor','course_code').first()
    taken = request.user.courses.filter(course_university_slug=course_university_slug,course_code=course_code,course_instructor_slug=course_instructor_slug).exists()
    if request.method == 'POST':
        form = ReviewForm(request.POST or None)
        if form.is_valid():
            review = form.save(False)
            review.author = request.user
            review.save()
            course.course_reviews.add(review)
    else:
        form = ReviewForm
    if request.is_ajax():
        data['reviews_count'] = course.reviews_count()
        data['reviews_all_count'] = course.reviews_all_count()
        data['review'] = render_to_string('home/courses/new_review.html',{'review': review},request=request)
        return JsonResponse(data)
    reviews_count = course.reviews_count()
    reviews_all_count = course.reviews_all_count()
    reviews = course.get_reviews()
    reviews_all = course.get_reviews_all()
    context = {
        'course':course,
        'reviews_count':reviews_count,
        'reviews_all_count':reviews_all_count,
        'reviews':reviews,
        'reviews_all':reviews_all,
        'taken':taken,
        'form':form,
    }
    return render(request,'home/courses/course_detail.html', context)  

# Template needs to be added
@login_required
def course_share(request,id):
    data = dict()
    course = get_object_or_404(Course, id=id)
    if request.method == 'POST':
        title = request.user.get_full_name() + " just started taking a course!"
        content = "Hey! I am taking " + course.course_code + " with professor " + course.course_instructor + "!"
        author = request.user
        post = Post(title=title,content=content,author=author)
        post.save()
        data['html'] = render_to_string('home/courses/course_shared.html',{'course':course},request=request)
        data['message'] = "Shared successfuly!"
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
def review_like(request,id,status=None):
    data = dict()
    review = get_object_or_404(Review, id=id)
    user = request.user
    if request.method == "POST":
        if status=="like":
            review.likes.add(user)
        elif status=="dislike":
            review.dislikes.add(user)
        elif status=="rmvlike":
            review.likes.remove(user)
        elif status == "rmvdislike":
            review.dislikes.remove(user)
        elif status == "ulike":
            review.dislikes.remove(user)
            review.likes.add(user)
        elif status == "udislike":
            review.likes.remove(user)
            review.dislikes.add(user)
        data['review'] = render_to_string('home/courses/review_like.html',{'review':review},request=request)
        return JsonResponse(data)

@login_required
def university_detail(request, course_university_slug):
    courses = Course.objects.filter(course_university_slug__icontains=course_university_slug)
    users = courses.select_related('profiles')
    course_instructors = courses.order_by('course_instructor','course_code','course_year').distinct('course_instructor','course_code')
    context = {
        'courses':courses,
        'users':users,
        'course_instructors':course_instructors,
    }
    return render('home/courses/univerist_detail.html',context,request)
            
'''

Method to returm related to students to user based on user courses taken
to be implemented after friending method

'''
@login_required
def related_students(request):
    pass        

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
def remove_saved_course(request,id):
    data = dict()
    course = get_object_or_404(Course, id=id)
    if request.method == "POST":
        request.user.saved_courses.remove(course)
        data['message'] = course.course_code + " with professor " + course.course_instructor + " has been successfully removed from your saved courses"
        return JsonResponse(data)
        
        
@login_required
def saved_courses(request):
    courses = request.user.saved_courses.all()
    return render(request,'home/courses/user_saved_courses.html',{'courses':courses})