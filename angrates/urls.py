from django.conf.urls import url, include

from django.contrib import admin

import podcasts.views

urlpatterns = [
    url(r'^(?P<feed>650|910)/(?P<year>[0-9]{4})/(?P<month>[0-9]+)/$',
        podcasts.views.month_calendar,
        name="archive_month"),
    url(r'^(?P<feed>650|910)/(?P<year>[0-9]{4})/(?P<month>[0-9]+)/(?P<day>[0-9]+)/$',
        podcasts.views.HourDayArchiveView.as_view(month_format='%m'),
        name="archive_day"),
    url(r'^$', podcasts.views.home, name="home"),
    url(r'^(?P<feed>650|910)/$', podcasts.views.home, name='home'),
    url(r'^refresh/(?P<scraper>.+)/$', podcasts.views.do_refresh, name='do_refresh'),
    url(r'^clips/$', podcasts.views.clips, name='clips'),
    url(r'^rss/$', podcasts.views.rss, name='rss'),
    url(r'^podcast/$', podcasts.views.podcast, name='podcast'),
    url(r'^about/$', podcasts.views.about, name='about'),
    url(r'^archives/$', podcasts.views.archives, name='archives'),
    url(r'^search/$', podcasts.views.search, name='search'),
    url(r'^clips/(?P<key>.+)/$', podcasts.views.clips, name='clips'),
    url(r'^minical/(?P<feed>650|910)/(?P<year>[0-9]{4})/(?P<month>[0-9]+)/$',
        podcasts.views.minical,
        name="minical"),
    url(r'^robots.txt/$', podcasts.views.robots, name='robots'),
    url(r'^latest/$', podcasts.views.latest_day, name='latest_day'),
    url(r'^(?P<feed>650|910)/latest$', podcasts.views.latest_day, name='latest_day'),
    url(r'^admin/', admin.site.urls),
]
