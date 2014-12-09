from django.db import models
from django.contrib.auth.models import User
import datetime
import urlparse


weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
        'Saturday', 'Sunday']


class Episode(models.Model):
    date = models.DateField()
    def __unicode__( self ):
        return "%s (%s)" % (self.date, weekdays[self.date.weekday()])


class Hour(models.Model):
    episode = models.ForeignKey(
        'Episode',
    )

    hour_num = models.IntegerField()

    title = models.CharField(
        max_length=200,
    )

    description = models.CharField(
        max_length=500,
    )

    summary = models.CharField(
        max_length=500,
    )

    duration = models.CharField(
        max_length=20,
    )

    download_link = models.URLField(
        null=True,
        blank=True,
    )

    link_650 = models.URLField(
        null=True,
        blank=True,
    )

    link_910 = models.URLField(
        null=True,
        blank=True,
    )

    @property
    def timestamp(self):
        return datetime.datetime.combine(
            self.episode.date,
            datetime.time(12+self.hour_num)
        )

    @property
    def milliseconds(self):
        epoch = datetime.datetime.utcfromtimestamp(0)
        delta = self.timestamp - epoch
        return int(delta.total_seconds()) * 1000

    class Meta:
        ordering = ['hour_num']

    def __unicode__( self ):
        return "%s (H%s)" % (self.episode, self.hour_num)


class Clip(models.Model):
    name = models.CharField(
        max_length=200,
    )

    description = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )

    link = models.URLField(
        null=True,
        blank=True,
    )

    origin = models.ForeignKey(
        'Hour',
        null=True,
        blank=True,
    )

    key = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )

    created_date = models.DateTimeField(auto_now_add=True)

    modified_date = models.DateTimeField(auto_now=True)


    @property
    def embed_link(self):
        if not self.link:
            return None
        video_key = self.youtube_key
        if not video_key:
            return None
        ret = 'http://www.youtube.com/embed/%s?autoplay=true' % video_key
        if '#' in self.link:
            time = self.link.split('#')[1]
            time = time.replace('t=', 'start=')
            ret += '&' + time + '&autoplay=true'
        return ret

    @property
    def youtube_key(self):
        video_key = None
        query = urlparse.urlparse(self.link.strip())
        p = urlparse.parse_qs(query.query)
        if query.hostname == 'youtu.be':
            video_key = query.path[1:]
        if query.hostname in ('www.youtube.com', 'youtube.com'):
            if query.path == '/watch':
                video_key = p['v'][0]
            if query.path[:7] == '/embed/':
                video_key = query.path.split('/')[2]
            if query.path[:3] == '/v/':
                video_key = query.path.split('/')[2]
        return video_key


    @property
    def thumbnail_url(self):
        if self.youtube_key:
            return 'http://img.youtube.com/vi/%s/0.jpg' % self.youtube_key

    def __unicode__( self ):
        return self.key
