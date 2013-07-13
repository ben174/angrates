from django.db import models

class Episode(models.Model):
    date = models.DateField()

class Hour(models.Model):
    6AM = 0
    7AM = 1
    8AM = 2
    9AM = 3

    HOUR_CHOICES = (
        (6AM, '6:00 AM'),
        (7AM, '7:00 AM'),
        (8AM, '8:00 AM'),
        (9AM, '9:00 AM'),
    )

    episode = models.ForeignKey(
        model='Episode', 
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

    download_link = models.URLField( )
