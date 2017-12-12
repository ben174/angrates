import datetime

from podcasts.models import AirDate, Hour
from django.core.management.base import BaseCommand

from podcasts.util.scraper import FeedScraper, LogLevels


class Command(BaseCommand):
    help = 'Scrapes the podcast feeds and loads each hour into the db.'

    def add_arguments(self, parser):
        parser.add_argument('--feed',
            action='store',
            default='both',
            help='Feed ("650" or "910" or "iheart" or "both")')

    def handle(self, *args, **options):
        scraper = FeedScraper()
        level_mapping = {
            LogLevels.ERROR: self.style.ERROR,
            LogLevels.SUCCESS: self.style.SUCCESS,
            LogLevels.WARNING: self.style.WARNING,
        }
        scrapes = []
        if options['feed'] == '650' or options['feed'] == 'both':
            #scrapes.append(scraper.scrape_650)
            pass
        if options['feed'] == '910' or options['feed'] == 'both':
            # scrapes.append(scraper.scrape_910)
            pass
        if options['feed'] == 'audioboom' or options['feed'] == 'both':
            scrapes.append(scraper.scrape_audioboom)
        if options['feed'] == 'iheart' or options['feed'] == 'both':
            scrapes.append(scraper.scrape_iheart)
        for scrape in scrapes:
            for log_line in scrape():
                self.stdout.write(level_mapping[log_line[0]](log_line[1]))

        # from podcasts.util import reddit
        # airdate = AirDate.objects.latest('pub_date')
        # red = reddit.Reddit(airdate)
        # red.connect()
        # if airdate.reddit_post_id:
        #     red.update_post()
        # else:
        #     red.create_post()

        # tweet_date = datetime.date.today()

        # untweeted_hours = Hour.objects.filter(
        #     tweeted=False,
        #     pub_date__gte=tweet_date,
        #     pub_date__lt=tweet_date + datetime.timedelta(days=1)
        # ).order_by('pub_date')

        # from podcasts.util import tweet
        # twitter = tweet.Twitter()
        # twitter.connect()
        # for hour in untweeted_hours:
        #     print 'Tweeting hour: {}'.format(hour)
        #     twitter.post_hour(hour)
