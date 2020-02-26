from django.conf.urls import url
from django.urls import path
from main import views
# SET THE NAMESPACE!
app_name = 'main'

#main:NAME goes in here - Reverse
urlpatterns=[
    path('signup/',views.signup,name='signup'),
    path('user_login',views.user_login,name='user_login'),
    path('',views.main_page,name='main_page'),
    path('home/', views.home, name='home'),
]