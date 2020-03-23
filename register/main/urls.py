from django.conf.urls import url
from django.urls import path,include
from main import views
from django.contrib.auth import views as auth_views
# SET THE NAMESPACE!
app_name = 'main'

urlpatterns=[
    path('signup/',views.signup,name='signup'),
    path('',views.user_login, name='user_login'),
    path('signout', views.user_logout, name='user_logout'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('', include('django.contrib.auth.urls')),
]