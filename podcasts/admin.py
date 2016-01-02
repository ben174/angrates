from django.contrib import admin

from podcasts.models import Hour, Clip

admin.site.register([Hour, Clip])
