from django.conf.urls import url
from django.urls import path, include
from home import views

urlpatterns = [
    path('',views.PostListView.as_view(), name='home'),
    path('post/<int:pk>/', views.post_detail, name='post-detail'),
    path('<int:pk>/like/', views.PostLikeToggle.as_view(), name='like-toggle'),
    path('api/<int:pk>/like/', views.PostLikeAPIToggle.as_view(), name='like-api-toggle'),
    path('post/<int:id>/update/', views.post_update, name='post-update'),
    path('post/<int:id>/delete/', views.post_delete, name='post-delete'),
    path('post/create/', views.post_create, name='post-create'),
  ]
