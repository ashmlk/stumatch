from django.conf.urls import url
from django.urls import path,include
from main import views
from django.contrib.auth import views as auth_views
# SET THE NAMESPACE!
app_name = 'main'

#main:NAME goes in here - Reverse
urlpatterns=[
    path('signup/',views.signup,name='signup'),
    path('login',views.user_login,name='user_login'),
    path('', views.user_logout, name='user_logout'),
    path('',views.main_page,name='main_page'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('', include('django.contrib.auth.urls')),
    
]