from django.conf.urls import url
from django.urls import path,include
from main import views
from django.contrib.auth import views as auth_views
from .models import BookmarkBlog, BookmarkBuzz, BookmarkPost
# SET THE NAMESPACE!
app_name = 'main'

urlpatterns=[
    path('signup/',views.signup,name='signup'),
    path('',views.user_login, name='user_login'),
    path('signout', views.user_logout, name='user_logout'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('', include('django.contrib.auth.urls')),
    path('bookmarks/', views.bookmarks,name='bookmarks'),
    path('bookmark/<str:hid>/<str:obj_type>/', views.add_bookmark,name='add-bookmark'),
    path('tags/posts/fav/<slug:slug>', views.f_post_tag,name='fav-post-tag'),
    path('tags/buzzes/fav/<slug:slug>', views.f_buzz_tag,name='fav-buzz-tag'),
    path('tags/blogs/fav/<slug:slug>', views.f_blog_tag,name='fav-blog-tag'),
    path('friends/', views.friends_main,name='friends-main'),
    path('find/program/', views.user_same_program,name='find-program'),
    path('friends/requests/', views.friend_requests,name='friend-requests'),
    path('friends/requests/pending/', views.friend_pending_requests,name='friend-pending'),
    path('friends/request/<str:hid>/action/<str:s>', views.accept_reject_friend_request,name='accept-reject-friend-request'),
    path('friends/<str:hid>/<str:s>/', views.add_remove_friend,name='add-rmv-friend'),
]