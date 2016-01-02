from django.core.management.base import BaseCommand

from podcasts.util.scraper import ClipScraper, LogLevels


class Command(BaseCommand):
    help = 'Scrapes the clip spreadsheet and loads each clip into the db.'

    def handle(self, *args, **options):
        scraper = ClipScraper()
        level_mapping = {
            LogLevels.ERROR: self.style.ERROR,
            LogLevels.SUCCESS: self.style.SUCCESS,
            LogLevels.WARNING: self.style.WARNING,
        }
        for log_line in scraper.load_clips():
            self.stdout.write(level_mapping[log_line[0]](log_line[1]))
