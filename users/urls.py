from django.conf.urls import patterns, include, url
from users import views

urlpatterns = patterns('',
    url(r'^$', views.users, name='users'),
    url(r'^\d+/$', views.user, name='user'),
    # url(r'^byname/^$', views.userbyname, name='userbyname'),
    # url(r'^\d+/songs/$', views.usersongs, name='usersongs'),
)
