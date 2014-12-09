# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('guide', '0002_clip_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='clip',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 8, 9, 29, 29, 985908), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='clip',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 8, 9, 29, 41, 690027), auto_now=True),
            preserve_default=False,
        ),
    ]
