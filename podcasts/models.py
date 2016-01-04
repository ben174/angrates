from __future__ import unicode_literals

import re
import urlparse

from django.db import models


class Hour(models.Model):
    FEED_CHOICES = (
        ('650', 'Talk 650 KSTE (Sac)'),
        ('910', 'Talk 910 KKSF (SF)')
    )

    pub_date = models.DateTimeField()

    feed = models.CharField(
        max_length=3,
        choices=FEED_CHOICES,
        null=False,
        blank=False,
    )

    title = models.CharField(
        max_length=600,
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

    link = models.URLField(
        null=True,
        blank=True,
        max_length=600,
    )

    class Meta:
        ordering = ['pub_date']

    @classmethod
    def _clean_title(cls, title):
        title = re.sub(r"(?i)^Armstrong and Getty(.*)$", "\g<1>", title)
        title = re.sub(r"(?i)^[0-9]{6}(.*)$", "\g<1>", title)
        title = re.sub(r"^[0-9]*\-[0-9]*\-[0-9]*\s(.*)$", "\g<1>", title)
        title = re.sub(r"(?i)^(?i)[0-9]\s?[AP]M[\s\-]+(.*)$", "\g<1>", title)
        return title

    def get_alternate_feeds(self):
        return Hour.objects.filter(pub_date=self.pub_date).exclude(pk=self.pk)

    def save(self, *args, **kwargs):
        self.title = Hour._clean_title(self.title)
        super(Hour, self).save(*args, **kwargs)

    def __unicode__(self):
        title = self.title
        if len(title) > 60:
            title = title[:57] + '...'
        return '{}-{}-{} - {} - {}'.format(
            self.pub_date.year,
            self.pub_date.month,
            self.pub_date.day,
            self.feed,
            title
        )


class Clip(models.Model):
    name = models.CharField(
        max_length=600,
    )

    description = models.CharField(
        max_length=2000,
        null=True,
        blank=True,
    )

    link = models.URLField(
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

    def __unicode__(self):
        return self.key
