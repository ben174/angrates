from __future__ import unicode_literals

import re
import urlparse
import datetime

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from podcasts.util import reddit


class AirDate(models.Model):
    pub_date = models.DateField(unique=True)
    reddit_post_id = models.CharField(max_length=20, null=True, blank=True)
    reddit_url = models.URLField(max_length=255, null=True, blank=True)

    def get_hours(self):
        base_date = datetime.date(
            self.pub_date.year,
            self.pub_date.month,
            self.pub_date.day,
        )
        hours = Hour.objects.filter(
            pub_date__gte=base_date,
            pub_date__lt=base_date+datetime.timedelta(days=1)
        ).order_by('pub_date')
        return hours

    def __unicode__(self):
        return str(self.pub_date)


class Hour(models.Model):
    FEED_CHOICES = (
        ('650', 'Talk 650 KSTE (Sac)'),
        ('910', 'Talk 910 KKSF (SF)')
    )

    pub_date = models.DateTimeField()
    air_date = models.ForeignKey(AirDate, null=True, blank=True)

    feed = models.CharField(
        max_length=3,
        choices=FEED_CHOICES,
        null=False,
        blank=False,
    )

    title = models.CharField(
        max_length=600,
        help_text="A short title for this segment. Shown in calendar view.",
    )

    description = models.CharField(
        max_length=500,
        help_text="A longer description of this segment. Only shown in day view.",
    )

    summary = models.CharField(
        max_length=500,
        help_text="NOT CURRENTLY USED",
    )

    duration = models.CharField(
        max_length=20,
        null=True,
        blank=True,
    )

    link = models.URLField(
        null=True,
        blank=True,
        max_length=600,
        help_text="Download URL",
    )

    best_of = models.BooleanField(
        default=False,
        help_text="Indicates this is a Best Of show, which is a compliation of segments from previous shows.",
    )

    class Meta:
        ordering = ['pub_date']
        unique_together = ['feed', 'pub_date']

    @classmethod
    def _clean_title(cls, title):
        title = re.sub(r"(?i)^Armstrong and Getty(.*)$", "\g<1>", title)
        title = re.sub(r"(?i)^[0-9]{6}(.*)$", "\g<1>", title)
        title = re.sub(r"^[0-9]*\-[0-9]*\-[0-9]*\s(.*)$", "\g<1>", title)
        title = re.sub(r"(?i)^(?i)[0-9]\s?[AP]M[\s\-]+(.*)$", "\g<1>", title)
        return title

    def get_alternate_feeds(self):
        return Hour.objects.filter(pub_date=self.pub_date).exclude(pk=self.pk)

    def get_airdate(self):
        air_date, _ = AirDate.objects.get_or_create(pub_date=self.pub_date)
        return air_date

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

@receiver(post_save, sender=Hour)
def reddit_discussion(sender, instance, **kwargs):
    # no op
    return
    airdate = instance.get_airdate()
    red = reddit.Reddit(airdate)
    red.connect()
    if airdate.reddit_post_id:
        red.update_post()
    else:
        red.create_post()


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
