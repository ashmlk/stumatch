from django.conf.urls import url
from django.urls import path, include
from home import views
# removed trailing backslashes
urlpatterns = [
    path('post/create/', views.post_create, name='post-create'),
    url(r'^$',views.home, name='home'),
    #path('post/<int:pk>/', views.post_detail, name='post-detail'),
    path('<int:pk>/like/', views.PostLikeToggle.as_view(), name='like-toggle'),
    path('api/<int:pk>/like/', views.PostLikeAPIToggle.as_view(), name='like-api-toggle'),
    path('post/update/<int:id>/', views.post_update, name='post-update'),
    path('post/delete/<int:id>/', views.post_delete, name='post-delete'),
    path('post/upload/image/', views.PostImageUpload.as_view(), name='post-image-upload'),
    
    path('courses/', views.courses_list, name='courses-list'),
    path('courses/add', views.courses_add, name='courses-add'),
    path('courses/delete/<int:id>', views.courses_delete, name='courses-delete'),
    
  ]
