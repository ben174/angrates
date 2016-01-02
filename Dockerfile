FROM python:2-onbuild
RUN ./manage.py collectstatic --noinput
RUN ./manage.py refresh_feeds
RUN ./manage.py refresh_clips
CMD gunicorn -b 0.0.0.0:8117 angrates.wsgi
EXPOSE 8117
