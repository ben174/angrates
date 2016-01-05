import json

import datetime

import os
from angrates import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from podcasts.models import Hour


class Command(BaseCommand):
    help = 'Loads the old clips from the 2.0 site (from json files)'

    def add_arguments(self, parser):
        parser.add_argument('--delete',
                            action='store_true',
                            default=False,
                            help='Overrite existing episodes.')

    def handle(self, *args, **options):
        self.stdout.write('Loading old JSON files')
        data_dir = os.path.join(settings.BASE_DIR, 'data/old')
        with open(os.path.join(data_dir, 'episodes.json'), 'r') as f:
            data = json.load(f)
        self.stdout.write(self.style.SUCCESS('Loaded episodes.json'))
        episodes = {}
        for episode in data:
            episodes[episode['pk']] = episode['fields']['date']
        self.stdout.write(self.style.SUCCESS('Loaded hours.json'))
        with open(os.path.join(data_dir, 'hours.json'), 'r') as f:
            data = json.load(f)
        for hour in data:
            episode_id = hour['fields']['episode']
            date = episodes.get(episode_id)
            if not date:
                self.stdout.write(self.style.ERROR('Unable to determine date for : {}'.format(episode_id)))
                continue
            y, m, d = [int(x) for x in date.split('-')]
            h = 5+hour['fields']['hour_num']

            pub_date = datetime.datetime(y, m, d, h, 0, 0)

            if Hour.objects.filter(pub_date=pub_date).exists():
                if options['delete']:
                    self.stdout.write(self.style.WARNING('Deleting hour: {}'.format(pub_date)))
                    Hour.objects.filter(pub_date=pub_date).delete()
                else:
                    self.stdout.write(self.style.WARNING('Episode already exists, will not overwrite: {}'.format(pub_date)))
                    continue
            h = Hour.objects.create(pub_date=pub_date)
            h.description = hour['fields']['description']
            h.title = hour['fields']['summary']
            h.summary = hour['fields']['summary']
            h.link = hour['fields']['download_link']
            h.duration = hour['fields']['duration']
            h.feed = '910'
            h.save()
            self.stdout.write(self.style.SUCCESS('Created hour: {}'.format(h)))
        self.stdout.write(self.style.SUCCESS('Restored old episodes.'))