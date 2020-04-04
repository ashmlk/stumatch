from django.conf.urls import url
from django.urls import path, include
from home import views
# removed trailing backslashes
urlpatterns = [
    url(r'^$',views.home, name='home'),
    path('post/create/', views.post_create, name='post-create'),
    path('p=<str:guid_url>/', views.post_detail, name='post-detail'),
    path('post/like/<str:guid_url>/', views.post_like, name='post-like'),
    path('post/update/<str:guid_url>/', views.post_update, name='post-update'),
    path('post/delete/<str:guid_url>/', views.post_delete, name='post-delete'),
    path('courses/', views.course_list, name='courses-list'),
    path('courses/add/', views.course_add, name='courses-add'),
    path('courses/delete/<int:id>', views.course_delete, name='courses-delete'),
  ]
