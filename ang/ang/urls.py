from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ang.views.home', name='home'),
    # url(r'^ang/', include('ang.foo.urls')),

    url(r'^calendar/(?P<year>\d+)/(?P<month>\d+)$', 'episodes.views.home', name="home"),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'episodes.views.home', name='home'), 
)
