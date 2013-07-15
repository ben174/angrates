from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

import datetime
import calendar

from episodes.models import Episode, Hour


def listing(request): 
    q = request.GET.get('q', '')
    hours = Hour.objects.filter(description__icontains=q, 
        summary__icontains=q,
    ).order_by('episode__date', 'hour_num')
    return render(request, 'episodes/listing.html', {
        'search': q, 
        'hours': hours, 
    })



def today(request): 
    today = datetime.datetime.now()
    return HttpResponseRedirect(reverse('episode', args=[today.year, today.month, today.day]))


def episode(request, year, month, day): 
    this_date = datetime.datetime(int(year), int(month), int(day))
    next_date = this_date + datetime.timedelta(days=1)
    prev_date = this_date - datetime.timedelta(days=1)
    try:
        episode = Episode.objects.get(date=this_date)
    except Episode.DoesNotExist:
        episode = None
    return render(request, 'episodes/episode.html', {
        'episode': episode, 
        'this_date': this_date, 
        'next_date': next_date, 
        'prev_date': prev_date, 
    })


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


