from podcasts.models import AirDate
from django.core.management.base import BaseCommand

from podcasts.util.scraper import FeedScraper, LogLevels


class Command(BaseCommand):
    help = 'Scrapes the podcast feeds and loads each hour into the db.'

    def add_arguments(self, parser):
        parser.add_argument('--feed',
            action='store',
            default='both',
            help='Feed ("650" or "910" or "both")')

    def handle(self, *args, **options):
        scraper = FeedScraper()
        level_mapping = {
            LogLevels.ERROR: self.style.ERROR,
            LogLevels.SUCCESS: self.style.SUCCESS,
            LogLevels.WARNING: self.style.WARNING,
        }
        scrapes = []
        if options['feed'] == '650' or options['feed'] == 'both':
            scrapes.append(scraper.scrape_650)
        if options['feed'] == '910' or options['feed'] == 'both':
            scrapes.append(scraper.scrape_910)
        for scrape in scrapes:
            for log_line in scrape():
                self.stdout.write(level_mapping[log_line[0]](log_line[1]))

        from podcasts.util import reddit
        airdate = AirDate.objects.latest('pub_date')
        red = reddit.Reddit(airdate)
        red.connect()
        if airdate.reddit_post_id:
            red.update_post()
        else:
            red.create_post()
