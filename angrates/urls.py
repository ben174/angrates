from django.conf.urls import url, include

from django.contrib import admin

import podcasts.views

urlpatterns = [
    url(r'^(?P<feed>650|910)/(?P<year>[0-9]{4})/(?P<month>[0-9]+)/$',
        podcasts.views.month,
        name="archive_month"),
    url(r'^(?P<feed>650|910)/(?P<year>[0-9]{4})/(?P<month>[0-9]+)/(?P<day>[0-9]+)/$',
        podcasts.views.HourDayArchiveView.as_view(month_format='%m'),
        name="archive_day"),
    url(r'^$', podcasts.views.home, name="home"),
    url(r'^(?P<feed>650|910)/$', podcasts.views.home, name='home'),
    url(r'^refresh/(?P<scraper>.+)/$', podcasts.views.do_refresh, name='do_refresh'),
    url(r'^clips/$', podcasts.views.clips, name='clips'),
    url(r'^about/$', podcasts.views.about, name='about'),
    url(r'^clips/(?P<key>.+)/$', podcasts.views.clips, name='clips'),
    url(r'^admin/', admin.site.urls),
]
