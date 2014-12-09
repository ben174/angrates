from django.shortcuts import render
from django.http import HttpResponse
import datetime
import calendar
from guide.models import Episode, Hour, Clip
import json


def listing(request):
    q = request.GET.get('q', '')
    hours = Hour.objects.filter(description__icontains=q,
        summary__icontains=q,
    ).order_by('episode__date', 'hour_num')
    print hours
    print 'ballsack'
    return render(request, 'listing.html', {
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
    return render(request, 'episode.html', {
        'episode': episode,
        'this_date': this_date,
        'next_date': next_date,
        'prev_date': prev_date,
    })


def bcal(request, year=None, month=None):
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

    return render(request, 'bcal.html', {
        'dates': dates,
        'month_date': month_date,
        'prev_month_date': prev_month_date,
        'next_month_date': next_month_date,
        'today': datetime.date.today(),
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

    return render(request, 'calendar.html', {
        'dates': dates,
        'month_date': month_date,
        'prev_month_date': prev_month_date,
        'next_month_date': next_month_date,
        'today': datetime.date.today(),
    })


def data(request): 
    from_dt = datetime.datetime.min
    to_dt = datetime.datetime.max
    if 'from' in request.GET:
        from_dt = datetime.datetime.utcfromtimestamp(int(request.GET.get('from'))/1000)
    if 'to' in request.GET:
        to_dt = datetime.datetime.utcfromtimestamp(int(request.GET.get('to'))/1000)
    hours = Hour.objects.filter(episode__date__gte=from_dt, episode__date__lte=to_dt)
    ret = {}
    ret['success'] = 1
    results = []
    for hour in hours:
        result = {}
        result['id'] = hour.pk
        result['title'] = hour.description
        result['url'] = hour.download_link
        result['class'] = 'event-info'
        result['start'] = hour.milliseconds
        result['end'] = hour.milliseconds + 3600000
        results.append(result)
    ret['result'] = results
    return HttpResponse(json.dumps(ret))


def clips(request):
    clips = Clip.objects.all()
    return render(request, 'clips.html', {
        'clips': clips,
    })


def clip(request, key):
    clip = Clip.objects.get(key=key)
    return render(request, 'clip.html', {
        'clip': clip,
    })

def search(request):
    query = request.GET.get('q', None)
    Clip.objects.filter()
