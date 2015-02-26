from django.conf.urls import patterns, include, url
from front import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),

    url(r'^editsong/$', views.editsong, name='editsong'),
    url(r'^songs/$', views.songs, name='songs'),
    url(r'^songs/\d+/$', views.song, name='song'),
    url(r'^backsongs/$', views.backsongs, name='songs'),
    url(r'^backsongs/\d+/$', views.backsong, name='song'),

    url(r'^edituser/$', views.edituser, name='edituser'),
    url(r'^users/$', views.users, name='users'),
    url(r'^users/\d+/$', views.user, name='user'),
    url(r'^backusers/$', views.backusers, name='users'),
    url(r'^backusers/\d+/$', views.backuser, name='user'),
)
