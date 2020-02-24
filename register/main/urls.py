from django.conf.urls import url
from main import views
# SET THE NAMESPACE!
app_name = 'main'
# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[
    url(r'^signup/$',views.signup,name='signup'),
    url(r'^user_login/$',views.user_login,name='user_login'),
]