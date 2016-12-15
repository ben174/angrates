from django.contrib import admin

from podcasts.models import Hour, Clip, AirDate

admin.site.register([Hour, Clip, AirDate])
