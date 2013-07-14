from django.db import models
from django.contrib.auth.models import User
from django.db.models import signals
from django.contrib.auth.management import create_superuser
from django.contrib.auth import models as auth_app
import datetime

# Prevent interactive question about wanting a superuser created.
signals.post_syncdb.disconnect(
    create_superuser,
    sender=auth_app,
    dispatch_uid = "django.contrib.auth.management.create_superuser"
)


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
        max_length=50, 
    )

    description = models.CharField(
        max_length=500, 
    )

    summary = models.CharField(
        max_length=200, 
    )

    duration = models.CharField(
        max_length=20,
    )

    download_link = models.URLField()
