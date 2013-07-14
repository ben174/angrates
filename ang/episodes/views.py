from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

import datetime
import calendar

from episodes.models import Episode, Hour


def home(request, year=None, month=None):
    try:
        year = int(year)
        month = int(month)
    except:
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
    dates = []
    hcal = calendar.HTMLCalendar(6)
    for d in hcal.itermonthdates(year, month):
        try:
            episode = Episode.objects.get(date=d)
        except Episode.DoesNotExist:
            episode = None
        dates.append((d, episode))

    month_date = datetime.date(year, month, 1)

    if month_date.month == 1:
        prev_month_date = datetime.date(year-1, 12, 1)
        next_month_date = datetime.date(year, month+1, 1)
    elif month_date.month == 12:
        next_month_date = datetime.date(year+1, 1, 1)
        prev_month_date = datetime.date(year, month-1, 1)
    else:
        prev_month_date = datetime.date(year, month-1, 1)
        next_month_date = datetime.date(year, month+1, 1)

    return render(request, 'episodes/calendar.html', {
        'dates': dates,
        'month_date': month_date,
        'prev_month_date': prev_month_date,
        'next_month_date': next_month_date,
        'today': datetime.date.today(),
    })


