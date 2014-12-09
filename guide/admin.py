from django.contrib import admin
from guide.models import Episode, Hour, Clip

# Register your models here.
admin.site.register([Episode, Hour, Clip])
