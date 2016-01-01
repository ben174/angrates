from django.views.generic.dates import MonthArchiveView

from podcasts.models import Hour

class HourMonthArchiveView(MonthArchiveView):
    queryset = Hour.objects.all()
    date_field = "pub_date"
    allow_future = True
    month_format = '%m'

