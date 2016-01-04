# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-03 19:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=600)),
                ('description', models.CharField(blank=True, max_length=2000, null=True)),
                ('link', models.URLField(blank=True, null=True)),
                ('key', models.CharField(blank=True, max_length=100, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Hour',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField()),
                ('feed', models.CharField(choices=[('650', 'Talk 650 KSTE (Sac)'), ('910', 'Talk 910 KKSF (SF)')], max_length=3)),
                ('title', models.CharField(max_length=600)),
                ('description', models.CharField(max_length=500)),
                ('summary', models.CharField(max_length=500)),
                ('duration', models.CharField(max_length=20)),
                ('link', models.URLField(blank=True, max_length=600, null=True)),
            ],
            options={
                'ordering': ['pub_date'],
            },
        ),
    ]
