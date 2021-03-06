import StringIO
import csv
import re
import string
import xml.etree.ElementTree as ET
import datetime
import dateutil

import requests

from podcasts.models import Hour, Clip


class LogLevels:
    SUCCESS = 'SUCCESS'
    WARNING = 'WARNING'
    ERROR = 'ERROR'


class FeedScraper:
    def scrape_650(self):
        xml_data = requests.get('http://www.kste.com/podcast/armandgettypodcast.xml').text
        root = ET.fromstring(xml_data)
        items = root.findall('channel/item')
        future_cutoff = datetime.datetime.now() + datetime.timedelta(days=1)
        for item in items:
            media_title = item.find('mediaTitle').text
            description = item.find('description').text
            description = re.sub('\s+', ' ', description).strip()
            title = item.find('title').text
            title = re.sub('\s+', ' ', title).strip()
            url = item.find('enclosure').attrib['url']
            dt = self._get_650_date(media_title)
            if not dt:
                yield LogLevels.ERROR, 'Error Parsing Title: ' + title
                continue
            if dt > future_cutoff:
                yield LogLevels.ERROR, 'Won\'t try to create an episode in the future'
                continue
            hour, created = Hour.objects.get_or_create(pub_date=dt, feed='650')
            # strips extra whitespace
            hour.description = description
            hour.title = title
            hour.link = url
            if not created:
                hour.save()
            if created:
                yield LogLevels.SUCCESS, 'Created: ' + str(hour)
            else:
                yield LogLevels.WARNING, 'Updated: ' + str(hour)

        yield LogLevels.SUCCESS, 'Successfully refreshed feed: 650'

    def scrape_910(self):
        xml_data = requests.get('http://www.talk910.com/podcast/ang2011.xml').text
        xml_data = xml_data.encode('utf-8').strip()
        import pdb
        pdb.set_trace()
        root = ET.fromstring(xml_data)
        items = root.findall('channel/item')

        future_cutoff = datetime.datetime.now() + datetime.timedelta(days=1)
        for item in items:
            description = item.find('description').text
            description = re.sub('\s+', ' ', description).strip()
            summary = item.find('{http://www.itunes.com/dtds/podcast-1.0.dtd}summary').text
            summary = re.sub('\s+', ' ', summary).strip()
            pub_date = item.find('pubDate').text
            title = item.find('title').text
            title = re.sub('\s+', ' ', title).strip()
            url = item.find('enclosure').attrib['url']
            dt = self._get_910_date(pub_date, title)
            if not dt:
                yield LogLevels.ERROR, 'Error Parsing Title: ' + title
                continue
            if dt > future_cutoff:
                yield LogLevels.ERROR, 'Won\'t try to create an episode in the future'
                continue
            hour, created = Hour.objects.get_or_create(pub_date=dt, feed="910")
            hour.description = description
            hour.title = summary
            hour.link = url
            hour.save()
            if created:
                yield LogLevels.SUCCESS, 'Created: ' + str(hour)
            else:
                yield LogLevels.WARNING, 'Updated: ' + str(hour)
        yield LogLevels.SUCCESS, 'Successfully refreshed feed: 910'

    def scrape_audioboom(self):
        xml_data = requests.get('https://audioboom.com/channels/4693403.rss').text
        xml_data = xml_data.encode('utf-8').strip()
        root = ET.fromstring(xml_data)
        items = root.findall('channel/item')
        future_cutoff = datetime.datetime.now() + datetime.timedelta(days=1)

        for item in items:
            description = item.find('title').text
            description = re.sub('\s+', ' ', description).strip()
            pub_date = item.find('pubDate').text
            title = item.find('title').text
            title = re.sub('\s+', ' ', title).strip()
            url = item.find('enclosure').attrib['url']
            dt = None
            try:
                dt = self._get_audioboom_date(pub_date, title)
                if dt.hour == 5:
                    # skip recap hour
                    continue
            except:
                pass
            if not dt:
                yield LogLevels.ERROR, 'Error Parsing Title: ' + title
                continue
            if dt > future_cutoff:
                yield LogLevels.ERROR, 'Won\'t try to create an episode in the future'
                continue
            hour, created = Hour.objects.get_or_create(pub_date=dt, feed="650")
            hour.description = description
            hour.title = title
            hour.link = url
            hour.save()

    def scrape_iheart(self):
        xml_data = requests.get('https://post.futurimedia.com/ksteam/playlist/rss/12.xml').text
        xml_data = xml_data.encode('utf-8').strip()
        root = ET.fromstring(xml_data)
        items = root.findall('channel/item')
        future_cutoff = datetime.datetime.now() + datetime.timedelta(days=1)

        for item in items:
            description = item.find('description').text
            description = re.sub('\s+', ' ', description).strip()
            pub_date = item.find('pubDate').text
            title = item.find('title').text
            title = re.sub('\s+', ' ', title).strip()
            url = item.find('enclosure').attrib['url']
            regex = r"^(\d+)\/(\d+)\/(\d+).*Hr\.\s(\d)\s(.*)$"
            try:
                m, d, y, h, title = re.findall(regex, title)[0]
            except:
                print 'Error parsing title: {}'.format(title)
                continue
            m, d, y, h = int(m), int(d), int(y) + 2000, int(h) + 5
            dt = datetime.datetime(y, m, d, h, 0, 0)

            # dt = self._get_iheart_date(pub_date, title)

            if not dt:
                yield LogLevels.ERROR, 'Error Parsing Title: ' + title
                continue
            if dt > future_cutoff:
                yield LogLevels.ERROR, 'Won\'t try to create an episode in the future'
                continue
            hour, created = Hour.objects.get_or_create(pub_date=dt, feed="650")
            hour.description = description
            hour.title = title
            hour.link = url
            print 'Created hour: {}'.format(dt)
            hour.save()

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
            return None

    def _get_audioboom_date(self, pub_date, title):
        dt = dateutil.parser.parse(title[:-4])
        return datetime.datetime(dt.year, dt.month, dt.day, int(title[-3]))

    def _get_iheart_date(self, pub_date, title):
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
            h = int(re.search(r'([0-9])AM', title).groups()[0])
            return datetime.datetime(y, m, d, h, 0, 0)
        except:
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


class ClipScraper:
    def load_clips(self):
        response = requests.get(
            'https://docs.google.com/spreadsheets/d/1Gq8ORD1x6DuzkxzAgEblrMUOLsZ3I4OvdWtkl-Vypj8/export?format=csv')
        if response.status_code != 200:
            yield LogLevels.ERROR, 'Google Docs returned a bad status code: ' + str(response.status_code)
        f = StringIO.StringIO(response.content)
        reader = csv.reader(f)
        for row in reader:
            row = [filter(lambda x: x in string.printable, c) for c in row]
            key = row[0]
            if key and key != 'Unique Key':
                clip, created = Clip.objects.get_or_create(key=key)
                if created:
                    yield LogLevels.SUCCESS, 'Created new clip: %s' % key
                name = row[1]
                description = row[2]
                link = row[3]
                # strip unicode characters
                name = name.decode('unicode_escape').encode('ascii', 'ignore')
                description = description.decode('unicode_escape').encode('ascii', 'ignore')
                link = link.decode('unicode_escape').encode('ascii', 'ignore')
                if clip.name != name or clip.description != description or clip.link != link:
                    yield LogLevels.SUCCESS, 'Updating clip: %s' % key
                    clip.name = row[1]
                    clip.description = row[2]
                    clip.link = row[3]
                    clip.save()
