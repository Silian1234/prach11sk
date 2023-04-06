from django import template
import datetime

register = template.Library()


@register.filter
def format_people(people):
    if people % 10 in [0, 1, 5, 6, 7, 8, 9] or people in [11, 12, 13, 14]:
        return 'человек'
    return 'человека'
