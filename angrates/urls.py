from django.conf.urls import url, include

from django.contrib import admin
from podcasts.views import HourMonthArchiveView, home

urlpatterns = [
    url(r'^(?P<feed>650|910)/(?P<year>[0-9]{4})/(?P<month>[0-9]+)/$',
        HourMonthArchiveView.as_view(month_format='%m'),
        name="archive_month"),
    url(r'^$', home, name="home"),
    url(r'^(?P<feed>650|910)/$', home, name="home"),
    url(r'^admin/', admin.site.urls),
]
# url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]+)/$', cal, name='calendar'),
'''
# Example: /2012/aug/
url(r'^(?P<year>[0-9]{4})/(?P<month>[-\w]+)/$',
    HourMonthArchiveView.as_view(),
    name="archive_month"),
# Example: /2012/08/
url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]+)/$',
    HourMonthArchiveView.as_view(month_format='%m'),
    name="archive_month_numeric"),
'''
