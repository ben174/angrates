"""
WSGI config for ang project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ang.settings")

from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

#from dj_static import Cling
#application = Cling(get_wsgi_application())
application = get_wsgi_application()
application = DjangoWhiteNoise(application)

