from django.contrib import admin
from episodes.models import Episode, Hour

admin.site.register([Episode, Hour])
