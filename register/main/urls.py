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
    path('settings/edit/', views.edit_profile, name='settings-edit'),
    path('update/profile/image/<str:hid>/', views.update_image, name='update-image'),
    path('remove/profile/image/<str:hid>/', views.remove_image, name='remove-image'),
    path('settings/privacy/', views.privacy_security, name='privacy-security'),
    path('settings/privacy/account/', views.set_public_private, name='set-public-private'),
    path('settings/privacy/password/', views.change_password, name='change-password'),
    path('settings/login_info/', views.login_info, name='login-info'),
    path('settings/blocked/', views.get_blocking, name='settings-blocked'),
    path('', include('django.contrib.auth.urls')),
    path('u/<str:username>/', views.get_user, name='get_user'),
    path('u/friends', views.get_user_friends, name='get_user_friends'),
    path('u/posts', views.get_user_posts, name='get_user_posts'),
    path('u/blogs', views.get_user_blogs, name='get_user_blogs'),
    path('u/courses', views.get_user_courses, name='get_user_courses'),
    path('bookmarks/', views.bookmarks,name='bookmarks'),
    path('bookmark/<str:hid>/<str:obj_type>/', views.add_bookmark,name='add-bookmark'),
    path('tags/<str:username>/', views.user_tags,name='usertags'),
    path('tags/posts/fav/<slug:slug>', views.f_post_tag,name='fav-post-tag'),
    path('tags/buzzes/fav/<slug:slug>', views.f_buzz_tag,name='fav-buzz-tag'),
    path('tags/blogs/fav/<slug:slug>', views.f_blog_tag,name='fav-blog-tag'),
    path('friends/', views.friends_main,name='friends-main'),
    path('find/program/', views.user_same_program,name='find-program'),
    path('friends/requests/', views.friend_requests,name='friend-requests'),
    path('friends/requests/pending/', views.friend_pending_requests,name='friend-pending'),
    path('friends/request/<str:hid>/action/<str:s>', views.accept_reject_friend_request,name='accept-reject-friend-request'),
    path('friends/<str:hid>/<str:s>/', views.add_remove_friend,name='add-rmv-friend'),
    path('block/<str:hid>/', views.block_user,name='block-user'),
    path('unblock/<str:hid>/', views.unblock_user,name='unblock-user'),
    path('your_notifications/', views.get_notifications,name='get-notifications'),
    path('your_notifications/mark_as_read', views.mark_notification_as_read,name='mark-notification-as-read'),
    path('your_notifications/delete', views.delete_notification,name='delete-notification'),
    
]