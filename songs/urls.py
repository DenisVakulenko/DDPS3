from django.conf.urls import patterns, include, url
from songs import views

urlpatterns = patterns('',
    # url(r'^$', views.index, name='index'),
    url(r'^$', views.songs, name='songs'),
    url(r'^\d+/$', views.song, name='song'),
)
