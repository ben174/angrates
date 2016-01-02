from __future__ import unicode_literals

import re

from django.db import models
import datetime



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

    link = models.URLField(
        null=True,
        blank=True,
    )

    '''
    @property
    def milliseconds(self):
        epoch = datetime.datetime.utcfromtimestamp(0)
        delta = self.timestamp - epoch
        return int(delta.total_seconds()) * 1000
    '''

    class Meta:
        ordering = ['pub_date']

    @classmethod
    def _clean_title(cls, title):
        title = re.sub(r"(?i)^Armstrong and Getty(.*)$", "\g<1>", title)
        title = re.sub(r"(?i)^[0-9]{6}(.*)$", "\g<1>", title)
        title = re.sub(r"^[0-9]*\-[0-9]*\-[0-9]*\s(.*)$", "\g<1>", title)
        title = re.sub(r"(?i)^(?i)[0-9]\s?[AP]M[\s\-]+(.*)$", "\g<1>", title)
        return title

    def save(self, *args, **kwargs):
        self.title = Hour._clean_title(self.title)
        super(Hour, self).save(*args, **kwargs)

    def __unicode__( self ):
        return Hour._clean_title(self.title)

