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

handler404 = 'main.views.handle_404'
#handler500 = 'main.views.handle_500'
#handler403 = 'main.views.handle_403'
#handler400 = 'main.views.handle_400'



urlpatterns = [ 
    #Has to be included for Forgot Password functionality on main page
    path('', include('django.contrib.auth.urls')), 
    url(r'^admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('ad235y9nv3nqb5b-AWRv0av3m-AtROYavm0mraM3RM350V/', admin.site.urls),    
    url(r'^taggit/', include('taggit_selectize.urls')),
    url(r'^ckeditor/upload/', login_required(ckeditor_views.upload), name='ckeditor_upload'),
    url(r'^ckeditor/browse/', never_cache(login_required(ckeditor_views.browse)), name='ckeditor_browse'),
    path('',views.user_login,name='user_login'),
    path('',include('main.urls'),name='main'), 
    path('accounts/', include('allauth.urls')), 
    url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
    # removed r'^home/' 
    url(r'',include(('home.urls','home'), namespace='home')),
    url(r'^friendship/', include('friendship.urls')),
    path('messages/', include('chat.urls', namespace='chat')),
        
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT ) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # + allauth_urlpatterns

'''
provider_urlpatterns = []

for provider in providers.registry.get_list():
    try:
        prov_mod = import_module(provider.get_package() + ".urls")
    except ImportError:
        continue
    prov_urlpatterns = getattr(prov_mod, "urlpatterns", None)
    if prov_urlpatterns:
        provider_urlpatterns += prov_urlpatterns

allauth_urlpatterns = [
    
    url(r"^accounts/password/change/$", allauth_views.password_change,name="account_change_password"),
    url(r"^accounts/password/set/$", allauth_views.password_set, name="account_set_password"),
    url(r"^accounts/inactive/$", allauth_views.account_inactive, name="account_inactive"),
    # E-mail
    url(r"^accounts/email/$", allauth_views.email, name="account_email"),
    url(r"^accounts/confirm-email/$", allauth_views.email_verification_sent,name="account_email_verification_sent"),
    url(r"^accounts/confirm-email/(?P<key>[-:\w]+)/$", allauth_views.confirm_email,name="account_confirm_email"),
    # password reset
    url(r"^accounts/password/reset/$", allauth_views.password_reset,name="account_reset_password"),
    url(r"^accounts/password/reset/done/$", allauth_views.password_reset_done,name="account_reset_password_done"),
    url(r"^accounts/password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",allauth_views.password_reset_from_key,name="account_reset_password_from_key"),
    url(r"^accounts/password/reset/key/done/$", allauth_views.password_reset_from_key_done,name="account_reset_password_from_key_done"),
    
] + provider_urlpatterns

'''