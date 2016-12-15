import datetime

from django.test import TestCase
from podcasts.util import reddit
from podcasts.models import Hour, AirDate



class ModelTest(TestCase):
    def test_hour_creates_airdate(self):
        Hour.objects.create(
            pub_date=datetime.datetime.now()-datetime.timedelta(hours=1),
            feed='910',
            title='Hour 1',
            summary='test',
            description='Description for hour 1'
        )
        Hour.objects.create(
            pub_date=datetime.datetime.now(),
            feed='910',
            title='Hour 2',
            summary='test',
            description='Description for hour 2'
        )
