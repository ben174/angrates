import calendar

from django.shortcuts import render
from django.views.generic.dates import MonthArchiveView
from podcasts.models import Hour


class HourMonthArchiveView(MonthArchiveView):
    queryset = Hour.objects.filter(feed='650')
    date_field = "pub_date"
    allow_future = True
    month_format = '%m'

    def get_context_data(self, **kwargs):
        context = super(HourMonthArchiveView, self).get_context_data(**kwargs)
        hcal = calendar.HTMLCalendar(6)
        iter = hcal.itermonthdates(int(self.get_year()), int(self.get_month()))
        context.update({'iter': iter})
        return context
