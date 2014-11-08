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

from ang import settings
from django.core.management import setup_environ

setup_environ(settings)

from episodes.models import *
from django.contrib.auth.models import User

import feedparser 


def main():
    create_admin()
    read_new_rss()


def read_rss(): 
    d = feedparser.parse('data/ang2011.xml')
    for entry in d.entries: 
        try: 
            create_hour(entry)
        except: 
            print "ERROR: ", entry.mediatitle
            print sys.exc_info()
            print traceback.format_exc()

def read_new_rss():
    d = feedparser.parse('data/armandgettypodcast.xml')
    for entry in d.entries: 
        #pprint.pprint(entry)

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
        hour = int(hour) - 5
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
                hour.download_link = entry.link
                hour.summary = entry.content[0]['value']
                print hour.summary
                hour.duration = entry.itunes_duration
                hour.title = entry.title
                hour.save()


        #print entry['summary']
        '''
        try: 
            create_hour(entry)
        except: 
            print "ERROR: ", entry.mediatitle
            print sys.exc_info()
            print traceback.format_exc()
        '''

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
