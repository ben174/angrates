#!/usr/bin/env python

import time
import os.path
from os.path import abspath, dirname, join
import sys
import datetime
import re
import traceback
import pprint

DIR = dirname(abspath(dirname(__file__)))
sys.path.append(DIR)

import feedparser 

import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ang.settings")
django.setup()

from ang import settings
from django.contrib.auth.models import User
from guide.models import *
import requests
import StringIO
import csv


def main():
    '''
    create_admin()
    read_rss()
    read_new_rss()
    '''
    load_clips()


def load_clips():
    response = requests.get('https://docs.google.com/spreadsheet/ccc?key=1Gq8ORD1x6DuzkxzAgEblrMUOLsZ3I4OvdWtkl-Vypj8&output=csv')
    assert response.status_code == 200, 'Wrong status code'
    f = StringIO.StringIO(response.content)
    reader = csv.reader(f)
    for row in reader:
        print row
        print 'Clip: %s' % row[0]
        key = row[0]
        if key and key != 'Unique Key':
            clip, created = Clip.objects.get_or_create(key=key)
            if created:
                print 'Created new clip: %s' % key
            name = row[1]
            description = row[2]
            link = row[3]
            if clip.name != name or clip.description != description or clip.link != link:
                print 'Updating clip: %s' % key
                clip.name = row[1]
                clip.description = row[2]
                clip.link = row[3]
                clip.save()



def read_rss():
    # http://www.talk910.com/podcast/ang2011.xml
    d = feedparser.parse('data/ang2011.xml')
    for entry in d.entries:
        pprint.pprint(entry)
        try:
            create_hour(entry)
        except:
            print "ERROR: ", entry.mediatitle
            print sys.exc_info()
            print traceback.format_exc()


def read_new_rss():
    # http://www.kste.com/podcast/armandgettypodcast.xml
    d = feedparser.parse('data/armandgettypodcast.xml')
    for entry in d.entries:
        pprint.pprint(entry)
        title = entry['mediatitle']
        date = None
        hour = None
        try:
            if ' ' in title:
                # old style
                _, date, hour = title.split(' ')
                hour = hour.replace('AM', '')
            else:
                # new style
                date = re.match("ang-(.*-.*-.*)-(.*)", title).group(1)
                hour = re.match("ang-(.*-.*-.*)-(.*)", title).group(2).replace('am', '')
        except:
            print 'Skipping', title
        try:
            hour = int(hour) - 5
        except:
            print 'Skipping', title
            continue

        if hour < 1 or hour > 4:
            print 'Bad hour'
            continue
        if date and hour:
            print date, hour
            m, d, y = [int(d) for d in date.split('-')]
            y = y + 2000
            dt = datetime.datetime(y,m,d)
            date = datetime.datetime.date(dt)
            print date
            episode, _ = Episode.objects.get_or_create(date=date)
            hour, created = Hour.objects.get_or_create(episode=episode, hour_num=hour)
            if created:
                hour.description = entry.summary
                hour.link_650 = entry.link
                hour.summary = entry.content[0]['value']
                print hour.summary
                hour.duration = entry.itunes_duration
                hour.title = entry.title
                hour.save()
            else:
                hour.link_650 = entry.link
                hour.save()


def create_hour(entry):
    _, _, _, date_string, hour_num = entry.mediatitle.split(' ')
    m, d, y = (int(date_string[0:2]), int(date_string[2:4]),
        int('20'+date_string[4:6]))
    dt = datetime.datetime(y,m,d)
    date = datetime.datetime.date(dt)
    hour_num = int(hour_num.replace('H',''))
    episode, _ = Episode.objects.get_or_create(date=date)

    hour, created = Hour.objects.get_or_create(episode=episode, hour_num=hour_num)
    if created:
        hour.description = entry.summary
        hour.link_910 = entry.link
        hour.summary = entry.content[0]['value']
        hour.duration = entry.itunes_duration
        hour.title = entry.title
        hour.save()
        print 'Hour create. Date: %s, Hour: %s' % (str(date), str(hour))
    else:
        print 'Hour already existed. Updating 910 link.'
        hour.link_910 = entry.link
        hour.save()


def create_admin():
    print "Creating user: admin"
    try:
        u = User.objects.create_user('admin', 'admin@admin.com', 'changeme')
        u.is_staff = True
        u.is_superuser = True
        u.save()
    except:
        print "Error creating admin."


if __name__ == '__main__':
    main()
