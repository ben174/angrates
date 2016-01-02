import re
import xml.etree.ElementTree as ET

import datetime
from django.core.management.base import BaseCommand, CommandError
from podcasts.models import Hour

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
          # Named (optional) arguments
        parser.add_argument('--feed',
            action='store',
            default='both',
            help='Feed ("650" or "910" or "both")')

    def handle(self, *args, **options):
        if options['feed'] == '650':
            self.scrape_650()
        elif options['feed'] == '910':
            self.scrape_910()
        elif options['feed'] == 'both':
            self.scrape_650()
            self.scrape_910()

    def scrape_650(self):
        tree = ET.parse('data/650.xml')
        root = tree.getroot()
        items = root.findall('channel/item')
        for item in items:
            media_title = item.find('mediaTitle').text
            description = item.find('description').text
            description = re.sub( '\s+', ' ', description ).strip()
            title = item.find('title').text
            title = re.sub( '\s+', ' ', title ).strip()
            url = item.find('enclosure').attrib['url']
            dt = self._get_650_date(media_title)
            if not dt:
                self.stdout.write(self.style.ERROR('Error Parsing Title: ' + title))
                continue
            hour, created = Hour.objects.get_or_create(pub_date=dt, feed='650')
            # strips extra whitespace
            hour.description = description
            hour.title = title
            hour.link = url
            hour.save()
            if created:
                self.stdout.write(self.style.SUCCESS('Created: ' + str(hour)))
            else:
                self.stdout.write(self.style.WARNING('Updated: ' + str(hour)))

        self.stdout.write(self.style.SUCCESS('Successfully refreshed.'))

    def scrape_910(self):
        tree = ET.parse('data/910.xml')
        root = tree.getroot()
        items = root.findall('channel/item')
        for item in items:
            media_title = item.find('mediaTitle').text
            description = item.find('description').text
            description = re.sub( '\s+', ' ', description).strip()
            summary = item.find('{http://www.itunes.com/dtds/podcast-1.0.dtd}summary').text
            summary = re.sub( '\s+', ' ', summary).strip()
            pub_date = item.find('pubDate').text
            title = item.find('title').text
            title = re.sub( '\s+', ' ', title ).strip()
            url = item.find('enclosure').attrib['url']
            dt = self._get_910_date(pub_date, title)
            if not dt:
                self.stdout.write(self.style.ERROR('Error Parsing Title: ' + title))
                continue
            hour, created = Hour.objects.get_or_create(pub_date=dt, feed="910")
            hour.description = description
            hour.title = summary
            hour.link = url
            hour.save()
            if created:
                self.stdout.write(self.style.SUCCESS('Created: ' + str(hour)))
            else:
                self.stdout.write(self.style.WARNING('Updated: ' + str(hour)))

    def _get_910_date(self, pub_date, title):
        months = {
            'Jan': 1,
            'Feb': 2,
            'Mar': 3,
            'Apr': 4,
            'May': 5,
            'Jun': 6,
            'Jul': 7,
            'Aug': 8,
            'Sep': 9,
            'Oct': 10,
            'Nov': 11,
            'Dec': 12,
        }
        title = re.sub('\s+', ' ', title).strip()
        try:
            d, m, y = re.search(r'.*,\s*([0-9]+)\s+(...)\s+([0-9]{4})', pub_date).groups()
            m = months[m]
            d, y = int(d), int(y)
            h = 5 + int(title[-1])
            return datetime.datetime(y, m, d, h, 0, 0)
        except:
            print title
            print m, d, y
            return None

    def _get_650_date(self, title):
        title = title[4:]
        try:
            m, d, y, h = title.split('-')
            m = int(m)
            d = int(d)
            y = 2000 + int(y)
            h = int(h[:-2])
            return datetime.datetime(y, m, d, h, 0, 0)
        except:
            return None
