from __future__ import unicode_literals
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

    def __unicode__( self ):
        return self.title

