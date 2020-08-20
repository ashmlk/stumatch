from django.conf.urls import url
from django.urls import path, include
from home import views


# removed trailing backslashes
urlpatterns = [
    url(r'^home/',views.home, name='home'),
    path('posts/trending', views.top_word_posts, name='top-word-post'),
    path('posts/hot/', views.hot_posts, name='hot-posts'),
    path('posts/top/', views.top_posts, name='top-posts'),
    path('posts/university/', views.uni_posts, name='uni-posts'),
    path('you/posts/', views.users_posts, name='users-posts'),
    path('you/buzzes/', views.users_buzzes, name='users-buzzes'),
    path('you/blogs/', views.users_blogs, name='users-blogs'),
    path('post/create/', views.post_create, name='post-create'),
    path('post/<str:guid_url>/', views.post_detail, name='post-detail'),
    path('post/<str:guid_url>/c/<str:hid>/like/', views.comment_like, name='comment-like'),
    path('post/<str:guid_url>/like/', views.post_like, name='post-like'),
    path('post/<str:guid_url>/update/', views.post_update, name='post-update'),
    path('post/<str:guid_url>/likes/', views.post_like_list, name='post-like-list'),
    path('post/<str:guid_url>/comments/', views.post_comment_list, name='post-comment-list'),
    path('post/<str:guid_url>/delete/', views.post_delete, name='post-delete'),
    path('post/comment/<str:hid>/delete/', views.comment_delete, name='comment-delete'),
    path('courses/', views.course_menu, name='course-menu'),
    path('courses/lists/', views.course_list, name='course-list'),
    path('courses/add/', views.course_add, name='courses-add'),
    path('course/auto/add/<slug:course_university_slug>/<slug:course_instructor_slug>/<str:course_code>/', views.course_auto_add, name='course-auto-add'),
    path('courses/saved/', views.saved_courses, name='courses-saved'),
    path('courses/share/<str:hid>/', views.course_share, name='course-share'),
    path('courses/saved/<int:id>/', views.course_save, name='course-save'),
    path('courses/saved/remove/<str:hid>/', views.remove_saved_course, name='course-save-remove'),
    path('courses/course/remove/<str:hid>/', views.course_remove, name='course-remove'),
    path('courses/<slug:par1>/instructor/<slug:par2>/', views.courses_instructor, name='course-instructor'),
    path('courses/<slug:course_university_slug>/<str:course_code>/instructors/', views.course_instructors, name='course-instructors'),
    path('courses/reviews/<str:hidc>/delete/<str:hid>/', views.review_delete, name='review-delete'),
    path('courses/<str:hidc>/reviews/<str:hid>/<str:status>/', views.review_like, name='review-like'),
    path('courses/<str:hid>/<str:code>/<str:status>/', views.course_vote, name='course-vote'),
    path('courses/reviews/<slug:course_university_slug>/<slug:course_instructor_slug>/<str:course_code>/', views.course_detail, name='course-detail'),
    path('university', views.university_detail, name='university-detail'),
    path('courses/mutual_students', views.get_course_mutual_students, name='course-mutual-students'),
    path('buzz/', views.buzz, name='buzz'),
    path('buzzes/hot/', views.hot_buzzes, name='hot-buzzes'),
    path('buzzes/top/', views.top_buzzes, name='top-buzzes'),
    path('buzzes/university/', views.uni_buzzes, name='uni-buzzes'),
    path('buzz/create/', views.buzz_create, name='buzz-create'),
    path('buzz/<str:guid_url>/like/<str:status>/', views.buzz_like, name='buzz-like'),
    path('buzz/<str:guid_url>/wot/<str:status>/', views.buzz_wot, name='buzz-wot'),
    path('buzz/<str:guid_url>/delete/', views.buzz_delete, name='buzz-delete'),
    path('buzz/i/<str:guid_url>/', views.buzz_detail, name='buzz-detail'),
    path('buzz/comments/<str:hid>/<str:status>/', views.comment_buzz_like, name='cbuzz-like'),
    path('buzz/delete/comments/<str:hid>/', views.comment_buzz_delete, name='cbuzz-delete'),
    path('blog/', views.blog, name='blog'),
    path('blog/create/', views.blog_create, name='blog-create'),
    path('blog/view/<str:hid>/<slug:t>/', views.blog_detail, name='blog-detail'),
    path('blog/edit/<str:hid>/<slug:t>/', views.blog_update, name='blog-edit'),
    path('blog/delete/<str:hid>/<slug:t>/', views.blog_delete, name='blog-delete'),
    path('blog/<str:guid_url>/like/', views.blog_like, name='blog-like'),
    path('blog/replies/<str:guid_url>/<slug:slug>/', views.blog_replies, name='blog-replies'),
    path('blog/replies/<str:guid_url>/<slug:slug>/edit/<str:hid>/', views.blog_reply_edit, name='blog-reply-edit'),
    path('blog/like/replies/<str:hid>/', views.blog_reply_like, name='blog-reply-like'),
    path('blog/<str:guid_url>/delete/reply/<str:hid>/', views.blog_reply_delete, name='blog-reply-delete'),
    path('posts/tag/<slug:slug>/', views.tags_post, name='tag-post'),
    path('blogs/tag/<slug:slug>/', views.tags_blog, name='tag-blog'),
    path('buzzes/tag/<slug:slug>/', views.tags_buzz, name='tag-buzz'),
    path('search', views.search, name='search-all'),
    path('search/results/get', views.search_dropdown, name='search-get'),
    path('search/results/user/remove', views.remove_search, name='remove-search-query'),
    path('find/students', views.find_students, name='find-students'),
    path('lists/', views.course_list_manager, name='course-list-manager'),
    path('lists/create/', views.course_list_create, name='course-list-create'),
    path('lists/delete/<str:hid>/', views.course_list_delete, name='course-list-delete'),
    path('lists/edit/<str:hid>/', views.course_list_edit, name='course-list-edit'),
    path('lists/<str:hid>', views.course_list_obj, name='course-list-obj'),
    path('lists/add/courses/<str:hid>/', views.course_list_obj_add_course, name='course-list-addcrs'),
    path('lists/courses/<str:hid>/remove/<str:hid_item>/', views.course_list_obj_remove_course, name='course-list-deletecrs'),
    path('lists/courses/<str:hid>/edit/<str:hid_item>/', views.course_list_obj_edit_course, name='course-list-editcrs'),
  ]
