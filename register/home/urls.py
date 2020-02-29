from django.conf.urls import url
from django.urls import path, include
from home import views

urlpatterns = [
    path('',views.home,name='home'), 
    url(r'^(?P<slug>[\w-]+)/$', views.PostDetail, name='post-detail'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
  ]


#post_detail for adding like:
# <p><a class='like-btn' data-href='{{ obj.get_api_like_url }}' data-likes='{{ obj.likes.count }}'  href='{{ obj.get_like_url }}'>{{ obj.likes.count }} Like</a></p>