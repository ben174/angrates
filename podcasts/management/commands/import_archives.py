import datetime

import urllib
from django.core.management.base import BaseCommand
from podcasts.models import Hour


class Command(BaseCommand):
    help = 'Imports archives from spreadsheets'

    def add_arguments(self, parser):
        parser.add_argument('--year',
            action='store',
            default='all',
            help='Year to import')

    def handle(self, *args, **options):
        years = ['2002', '2003', '2004', '2005', '2006']
        if options['year'] != 'all':
            years = [options['year']]
        for year in years:
            self.import_sheet(year)

    def import_sheet(self, year):
        filename = 'data/archive-sheets/{}.csv'.format(year)
        with open(filename) as f:
            lines = f.readlines()
            for line in lines:
                cells = line.split(',')
                if cells[0] == 'Filename':
                    # header cell
                    continue

                filename = cells[0].strip()
                if filename.startswith('./'):
                    filename = filename[2:]

                date_string = cells[1].strip()
                time_string = cells[2].strip()
                title = cells[3].strip()
                summary = cells[4].strip()
                description = cells[5].strip()
                best_of = cells[6].strip() == 'x'
                link = cells[7].strip()
                filename = urllib.quote(filename)
                link = 'https://storage.googleapis.com/ang-archives/{}/{}'.format(year, filename)

                try:
                    m, d, y = [int(x) for x in date_string.split('/')]
                    h, _ = time_string.split(':')
                    h = int(h)
                    date = datetime.datetime(y, m, d, h, 0, 0)
                    print date_string, time_string
                    print date
                    print link
                    print best_of
                    print
                except ValueError:
                    print 'Error parsing date: {}'.format(date_string)
                    continue

                if not title:
                    title = 'A&G Archives - {}'.format(date_string)
                if not summary:
                    summary = title
                if not description:
                    description = summary

                hour, created = Hour.objects.get_or_create(pub_date=date, feed='650')
                hour.link = link
                hour.title = summary
                hour.summary = summary
                hour.description = description
                hour.best_of = best_of
                hour.save()
