# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-15 11:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('podcasts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hour',
            name='best_of',
            field=models.BooleanField(default=False),
        ),
    ]
