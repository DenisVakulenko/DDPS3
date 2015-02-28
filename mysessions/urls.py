from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    url(r'^$', views.handle, name=''),
    url(r'^.*/$', views.handle, name=''),
    url(r'^check/$', views.check, name=''),
)
