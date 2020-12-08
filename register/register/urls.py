"""register URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from main import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
import friendship
import notifications.urls
import admin_honeypot
from django.conf.urls import handler400, handler403, handler404, handler500
from allauth.account import views as allauth_views
from allauth.socialaccount import views as allauth_socialviews
from allauth.socialaccount import providers
from importlib import import_module
from ckeditor_uploader import views as ckeditor_views
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from defender.decorators import watch_login

handler404 = 'main.views.handle_404'
#handler500 = 'main.views.handle_500'
#handler403 = 'main.views.handle_403'
#handler400 = 'main.views.handle_400'



urlpatterns = [ 
    path('', include('django.contrib.auth.urls')), 
    url(r'^admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('ad235y9nv3nqb5b-AWRv0av3m-AtROYavm0mraM3RM350V/', admin.site.urls),  
    url(r'^ad235y9nv3nqb5b-AWRv0av3m-AtROYavm0mraM3RM350V/defender/', include('defender.urls')),  
    url(r'^taggit/', include('taggit_selectize.urls')),
    url(r'^ckeditor/upload/', login_required(ckeditor_views.upload), name='ckeditor_upload'),
    url(r'^ckeditor/browse/', never_cache(login_required(ckeditor_views.browse)), name='ckeditor_browse'),
    path('',include('main.urls'),name='main'), 
    path('accounts/', include('allauth.urls')), 
    url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
    url(r'',include(('home.urls','home'), namespace='home')),
    url(r'^friendship/', include('friendship.urls')),
    #path('',views.user_login,name='user_login'),
        
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT ) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # + allauth_urlpatterns
