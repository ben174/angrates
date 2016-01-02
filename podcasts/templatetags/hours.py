import datetime
from django import template

from podcasts.models import Hour

register = template.Library()


@register.simple_tag
def current_time(format_string):
    return datetime.datetime.now().strftime(format_string)


@register.simple_tag
def hours_for(date, feed):
    return Hour.objects.filter(
        pub_date__month=date.month,
        pub_date__day=date.day,
        pub_date__year=date.year,
        feed=feed,
    )

@register.simple_tag
def has_hours(date):
    return Hour.objects.filter(
        pub_date__month=date.month,
        pub_date__day=date.day,
        pub_date__year=date.year,
    ).exists()

def cut(value, arg):
    """Removes all values of arg from the given string"""
    return value.replace(arg, '')


register.filter('cut', cut)
