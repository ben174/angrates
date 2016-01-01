import datetime
from django import template

from podcasts.models import Hour

register = template.Library()


@register.simple_tag
def current_time(format_string):
    return datetime.datetime.now().strftime(format_string)


@register.simple_tag
def hours_for(date, feed, object_list):
    return Hour.objects.filter(
        pub_date__month=date.month,
        pub_date__day=date.day,
        feed=feed,
    )
    return object_list.filter(
        pub_date__year=date.year,
        pub_date__month=date.month,
        pub_date__day=date.day,
    )


def cut(value, arg):
    """Removes all values of arg from the given string"""
    return value.replace(arg, '')


register.filter('cut', cut)
