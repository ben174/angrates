import calendar

import datetime
from django.views.generic.dates import MonthArchiveView
from podcasts.models import Hour


def home(request, feed='910'):
    today = datetime.date.today()
    return HourMonthArchiveView.as_view()(request,
                                          year=str(today.year - 1),
                                          month=str(today.month), feed=feed)


class HourMonthArchiveView(MonthArchiveView):
    queryset = Hour.objects.filter(feed='650')
    date_field = "pub_date"
    allow_future = True
    month_format = '%m'
    feed = '910'

    def get_context_data(self, **kwargs):
        context = super(HourMonthArchiveView, self).get_context_data(**kwargs)
        hcal = calendar.HTMLCalendar(6)
        iter = hcal.itermonthdates(int(self.get_year()), int(self.get_month()))
        context.update({
            'iter': iter,
            'feed': self.kwargs['feed']
        })
        return context
