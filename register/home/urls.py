from django.conf.urls import url
from django.urls import path, include
from home import views
# removed trailing backslashes
urlpatterns = [
    url(r'^$',views.home, name='home'),
    path('posts/latest/', views.latest_posts, name='latest-posts'),
    path('posts/<str:username>/', views.users_posts, name='users-posts'),
    path('post/create/', views.post_create, name='post-create'),
    path('post/<str:guid_url>/', views.post_detail, name='post-detail'),
    path('post/<str:guid_url>/like/', views.post_like, name='post-like'),
    path('post/<str:guid_url>/update/', views.post_update, name='post-update'),
    path('post/<str:guid_url>/likes/', views.post_like_list, name='post-like-list'),
    path('post/<str:guid_url>/comments/', views.post_comment_list, name='post-comment-list'),
    path('post/<str:guid_url>/c/<int:id>/like/', views.comment_like, name='comment-like'),
    path('post/<str:guid_url>/delete/', views.post_delete, name='post-delete'),
    path('courses/', views.courses, name='courses'),
    path('courses/add/', views.course_add, name='courses-add'),
    path('courses/course/remove/<int:id>/', views.course_remove, name='course-remove'),
    path('courses/<str:par1>/instructor/<str:par2>/', views.courses_instructor, name='course-instructor'),
    path('courses/<int:id>/<str:code>/<str:status>/', views.course_vote, name='course-vote'),
  ]
