from django.conf.urls import url
from django.urls import path,include
from main import views
from django.contrib.auth import views as auth_views
# SET THE NAMESPACE!
app_name = 'main'

#main:NAME goes in here - Reverse
urlpatterns=[
    path('signup/',views.signup,name='signup'),
    #remove user_login and change to login
    path('login',views.user_login,name='user_login'),
    path('',views.main_page,name='main_page'),
    path('<str:username>', views.home, name='home'),
    #replace home/edit with below
    path('<str:username>/edit', views.edit_profile, name='edit_profile'),
    path('<str:username>/password-reset', views.reset_password, name='reset_password'),
    path('main/', include('django.contrib.auth.urls')),
    
]