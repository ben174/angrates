#!/usr/bin/env python

import time
import os.path
from os.path import abspath, dirname, join
import sys
import datetime
import re
import traceback

DIR = dirname(abspath(dirname(__file__)))
sys.path.append(DIR)

from ang import settings
from django.core.management import setup_environ

setup_environ(settings)

from episodes.models import *
from django.contrib.auth.models import User

import feedparser 


def main():
    create_admin()
    read_rss()


def read_rss(): 
    d = feedparser.parse('data/ang2011.xml')
    for entry in d.entries: 
        try: 
            create_hour(entry)
        except: 
            print "ERROR: ", entry.mediatitle
            print sys.exc_info()
            print traceback.format_exc()


def create_hour(entry): 
    _, _, _, date_string, hour_num = entry.mediatitle.split(' ')
    m, d, y = (int(date_string[0:2]), int(date_string[2:4]), 
        int('20'+date_string[4:6]))
    dt = datetime.datetime(y,m,d)
    date = datetime.datetime.date(dt)
    hour_num = int(hour_num.replace('H',''))
    episode, _ = Episode.objects.get_or_create(date=date)
    
    created, hour = Hour.objects.get_or_create(episode=episode, hour_num=hour_num)
    if created: 
        hour.description = entry.summary
        hour.download_link = entry.link
        hour.summary = entry.content[0]['value']
        hour.duration = entry.itunes_duration
        hour.title = entry.title
        hour.save()
        print 'Hour create. Date: %s, Hour: %s' % (str(date), str(hour))
    else: 
        print 'Hour already existed. Skipping.'
    

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
