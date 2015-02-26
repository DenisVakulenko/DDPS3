from django.conf.urls import patterns, include, url
from django.contrib import admin



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'DDPS3.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^front/', include('front.urls')),
    url(r'^users/', include('users.urls')),
    url(r'^songs/', include('songs.urls')),
    # url(r'^mysessions/', include('mysessions.urls')),
)
