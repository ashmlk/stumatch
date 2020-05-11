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
    path('post/comment/<int:id>/delete/', views.comment_delete, name='comment-delete'),
    path('courses/', views.courses, name='courses'),
    path('courses/add/', views.course_add, name='courses-add'),
    path('courses/saved/', views.saved_courses, name='courses-saved'),
    path('courses/share/<int:id>/', views.course_share, name='course-share'),
    path('courses/saved/<int:id>/', views.course_save, name='course-save'),
    path('courses/saved/remove/<int:id>/', views.remove_saved_course, name='course-save-remove'),
    path('courses/course/remove/<int:id>/', views.course_remove, name='course-remove'),
    path('courses/<slug:par1>/instructor/<slug:par2>/', views.courses_instructor, name='course-instructor'),
    path('courses/<slug:course_university_slug>/<str:course_code>/instructors/', views.course_instructors, name='course-instructors'),
    path('courses/reviews/<int:id>/<str:status>/', views.review_like, name='review-like'),
    path('courses/<int:id>/<str:code>/<str:status>/', views.course_vote, name='course-vote'),
    path('courses/<slug:course_university_slug>/<slug:course_instructor_slug>/<str:course_code>/', views.course_detail, name='course-detail'),
  ]
