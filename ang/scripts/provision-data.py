#!/usr/bin/env python

import time
import os.path
from os.path import abspath, dirname, join
import sys
import datetime
import re

DIR = dirname(abspath(dirname(__file__)))
sys.path.append(DIR)

from ang import settings
from django.core.management import setup_environ

setup_environ(settings)

from episodes.models import *
from django.contrib.auth.models import User


def main():
    pass
