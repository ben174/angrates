import calendar

import datetime

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic.dates import MonthArchiveView, DayArchiveView
from podcasts.models import Hour, Clip
from podcasts.util import search as search_util
from podcasts.util.scraper import FeedScraper, ClipScraper


def home(request, feed='910'):
    today = datetime.date.today()
    return month(
        request,
        year=today.year,
        month=today.month,
        feed=feed,
    )


def month(request, year=None, month=None, feed='910'):
    if not year:
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
    date = datetime.datetime(int(year), int(month), 1)
    previous_month = date - datetime.timedelta(days=1)
    previous_month = datetime.datetime(previous_month.year, previous_month.month, 1)
    next_month = date + datetime.timedelta(days=31)
    next_month = datetime.datetime(next_month.year, next_month.month, 1)
    year = date.year
    month = date.month
    hcal = calendar.HTMLCalendar(6)
    iter = hcal.itermonthdates(year, month)
    object_list = Hour.objects.filter()
    today = datetime.date(
        datetime.datetime.now().year,
        datetime.datetime.now().month,
        datetime.datetime.now().day,
    )
    return render(request, 'podcasts/hour_archive_month.html', {
        'iter': iter,
        'hcal': hcal,
        'object_list': object_list,
        'feed': feed,
        'month': date,
        'previous_month': previous_month,
        'next_month': next_month,
        'today': today,
    })


class HourMonthArchiveView(MonthArchiveView):
    queryset = Hour.objects.all()
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
            'feed': self.kwargs['feed'],
        })
        return context


class HourDayArchiveView(DayArchiveView):
    queryset = Hour.objects.all()
    date_field = 'pub_date'
    allow_future = True
    month_format = '%m'
    feed = '910'

    def get_queryset(self):
        return Hour.objects.filter(feed=self.kwargs['feed'])

    def get_context_data(self, **kwargs):
        context = super(HourDayArchiveView, self).get_context_data(**kwargs)
        hcal = calendar.HTMLCalendar(6)
        iter = hcal.itermonthdates(int(self.get_year()), int(self.get_month()))
        today = datetime.date.today()
        context.update({
            'iter': iter,
            'feed': self.kwargs['feed'],
            'today': today,
        })
        return context


def clip_refresh_response_generator():
    yield 'Refreshing Clips: {}\n'.format(str(datetime.datetime.now()))
    scraper = ClipScraper()
    for log_line in scraper.load_clips():
        yield '{}: {}\n'.format(log_line[0], log_line[1])


def feed_refresh_response_generator():
    yield 'Refreshing Feeds: {}\n'.format(str(datetime.datetime.now()))
    scraper = FeedScraper()
    scrapes = scraper.scrape_650, scraper.scrape_910
    for scrape in scrapes:
        yield '{}\n{}\n'.format(scrape.__name__, '-' * 10)
        for log_line in scrape():
            yield '{}: {}\n'.format(log_line[0], log_line[1])
        yield '\n'


def do_refresh(request, scraper):
    response = ""
    if scraper == 'feeds' or scraper == 'both':
        response += "".join(feed_refresh_response_generator()) + "\n\n"
    if scraper == 'clips' or scraper == 'both':
        response += "".join(clip_refresh_response_generator()) + "\n\n"
    return HttpResponse(response, content_type='text/plain')

def clips(request, key=None):
    if key:
        clip = get_object_or_404(Clip, key=key)
        return render(request, 'clip.html', {'clip': clip})
    return render(request, 'clips.html', {'clips': Clip.objects.all()})

def minical(request, feed='910', year=None, month=None):
    if not year:
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
    date = datetime.datetime(int(year), int(month), 1)
    previous_month = date - datetime.timedelta(days=1)
    previous_month = datetime.datetime(previous_month.year, previous_month.month, 1)
    next_month = date + datetime.timedelta(days=31)
    next_month = datetime.datetime(next_month.year, next_month.month, 1)
    hcal = calendar.HTMLCalendar(6)
    iter = hcal.itermonthdates(date.year, date.month)
    today = datetime.date(
        datetime.datetime.now().year,
        datetime.datetime.now().month,
        datetime.datetime.now().day,
    )
    return render(request, 'blocks/minical.html', {
        'iter': iter,
        'feed': feed,
        'day': date,
        'today': today,
        'previous_month': previous_month,
        'next_month': next_month,
    })


def about(request):
    return render(request, 'about.html')


def search(request):
    query_string = request.GET.get('q', '')
    clips = None
    hours = None
    if query_string:
        clip_query = search_util.get_query(query_string, ['name', 'description'])
        hour_query = search_util.get_query(query_string, ['title', 'description'])
        clips = Clip.objects.filter(clip_query)
        hours = Hour.objects.filter(hour_query)
    return render(request, 'results.html', {
        'query': query_string,
        'clips': clips,
        'hours': hours,
    })


def verification(request):
    return HttpResponse('google-site-verification: google07b0b1ab3e57735f.html', content_type='text/plain')
