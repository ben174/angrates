# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clip',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200, null=True, blank=True)),
                ('link', models.URLField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Hour',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hour_num', models.IntegerField()),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=500)),
                ('summary', models.CharField(max_length=500)),
                ('duration', models.CharField(max_length=20)),
                ('download_link', models.URLField(null=True, blank=True)),
                ('link_650', models.URLField(null=True, blank=True)),
                ('link_910', models.URLField(null=True, blank=True)),
                ('episode', models.ForeignKey(to='guide.Episode')),
            ],
            options={
                'ordering': ['hour_num'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='clip',
            name='origin',
            field=models.ForeignKey(blank=True, to='guide.Hour', null=True),
            preserve_default=True,
        ),
    ]
