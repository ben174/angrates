import datetime
import calendar
import pytz

from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.views.generic.dates import MonthArchiveView, DayArchiveView
from feedgen.feed import FeedGenerator

from angrates import settings
from podcasts.models import Hour, Clip
from podcasts.util import search as search_util
from podcasts.util.scraper import FeedScraper, ClipScraper


def home(request, feed=settings.DEFAULT_FEED):
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    try:
        latest_episode = Hour.objects.latest('pub_date')
        year = latest_episode.pub_date.year
        month = latest_episode.pub_date.month
    except ObjectDoesNotExist:
        # no entries, just show empty calendar
        pass
    return month_calendar(
        request,
        year=year,
        month=month,
        feed=feed,
    )


def latest_day(request, feed=settings.DEFAULT_FEED):
    try:
        latest_episode = Hour.objects.latest('pub_date')
    except ObjectDoesNotExist:
        return HttpResponseNotFound("No podcasts in the database.")
    return HourDayArchiveView.as_view()(
        request=request,
        year=str(latest_episode.pub_date.year),
        month=str(latest_episode.pub_date.month),
        day=str(latest_episode.pub_date.day),
        feed=feed,
    )


def month_calendar(request, year=None, month=None, feed=settings.DEFAULT_FEED):
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
    today = datetime.date(
        datetime.datetime.now().year,
        datetime.datetime.now().month,
        datetime.datetime.now().day,
    )
    alt_feed = '650' if feed == '910' else '910'
    alt_link = reverse('archive_month', kwargs={
        'feed': alt_feed,
        'year': year,
        'month': month
    })
    has_alt = Hour.objects.filter(pub_date__gte=date, pub_date__lt=next_month, feed=alt_feed)
    return render(request, 'podcasts/hour_archive_month.html', {
        'iter': iter,
        'hcal': hcal,
        'feed': feed,
        'month': date,
        'has_alt': has_alt,
        'previous_month': previous_month,
        'next_month': next_month,
        'today': today,
        'alt_link': alt_link,
    })


class HourMonthArchiveView(MonthArchiveView):
    queryset = Hour.objects.all()
    date_field = "pub_date"
    allow_future = True
    month_format = '%m'
    feed = settings.DEFAULT_FEED

    def get_context_data(self, **kwargs):
        context = super(HourMonthArchiveView, self).get_context_data(**kwargs)
        hcal = calendar.HTMLCalendar(6)
        iter = hcal.itermonthdates(int(self.get_year()), int(self.get_month()))
        context.update({
            'iter': iter,
            'feed': self.kwargs['feed'],
        })
        return context


def _get_alt_feed_kwargs(kwargs):
    ret = kwargs.copy()
    alt_feed = '650' if kwargs['feed'] == '910' else '910'
    ret.update({'feed': alt_feed})
    return ret



class HourDayArchiveView(DayArchiveView):
    queryset = Hour.objects.all()
    date_field = 'pub_date'
    allow_future = True
    month_format = '%m'
    feed = settings.DEFAULT_FEED

    def get_queryset(self):
        return Hour.objects.filter(feed=self.kwargs['feed'])

    def get_context_data(self, **kwargs):
        context = super(HourDayArchiveView, self).get_context_data(**kwargs)
        hcal = calendar.HTMLCalendar(6)
        iter = hcal.itermonthdates(int(self.get_year()), int(self.get_month()))
        today = datetime.date.today()
        alt_link = reverse('archive_day', kwargs=_get_alt_feed_kwargs(self.kwargs))
        context.update({
            'iter': iter,
            'feed': self.kwargs['feed'],
            'today': today,
            'alt_link': alt_link,
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

def archives(request):
    return render(request, 'archives.html')

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


def robots(request):
    return HttpResponse('User-agent: *\nDisallow:', content_type='text/plain')


def rss(request):
    fg = FeedGenerator()
    fg.load_extension('podcast')
    fg.id('http://www.armstrongandgettybingo.com/rss')
    fg.podcast.itunes_category('News & Politics', 'Conservative (Right)')
    fg.podcast.itunes_explicit('no')
    fg.title('The Armstrong and Getty Show (Bingo)')
    fg.author( {'name':'Ben Friedland','email':'ben@bugben.com'} )
    fg.link( href='http://www.armstrongandgettybingo.com', rel='alternate' )
    fg.logo('https://s3-us-west-1.amazonaws.com/bencast/bingologo.png')
    fg.subtitle('Armstrong and Getty Bingo')
    fg.link( href='http://www.armstrongandgettybingo.com/rss', rel='self' )
    fg.language('en')
    pacific = pytz.timezone('America/Los_Angeles')

    for hour in Hour.objects.all().order_by('-pub_date'):
        fe = fg.add_entry()
        fe.id(hour.link)
        fe.title(hour.title)
        fe.description(hour.description)
        fe.enclosure(hour.link, 0, 'audio/mpeg')
        fe.published(pacific.localize(hour.pub_date))
    return HttpResponse(fg.rss_str(pretty=True), content_type='application/rss+xml')
