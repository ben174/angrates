from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^calendar/(?P<year>\d+)/(?P<month>\d+)$', 'guide.views.home', name="home"),
    url(r'^$', 'guide.views.home', name='home'), 
    url(r'^bcal$', 'guide.views.bcal', name='bcal'), 
    url(r'^listing/$', 'guide.views.listing', name='listing'), 
    url(r'^episode/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)$', 'guide.views.episode', name="episode"),
    url(r'^today/$', 'guide.views.today', name='today'), 
    url(r'^data/$', 'guide.views.data', name='data'), 
    url(r'^clips/$', 'guide.views.clips', name='clips'), 
    url(r'^clips/(?P<key>.+)$', 'guide.views.clip', name='clip'), 
    url(r'^search/$', 'guide.views.search', name='search'), 
    #(r'^search/', include('haystack.urls')),
)
