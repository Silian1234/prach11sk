from django import template
from datetime import datetime
from django.utils import timezone
register = template.Library()


@register.filter
def get_wash_status(date_time):
    return 'запланирована' if date_time.astimezone(timezone.get_current_timezone()) > datetime.now(tz=timezone.get_current_timezone()) else 'в процессе'

@register.filter
def is_today(date):
    return date == datetime.now().date()

@register.filter
def lt_time_now(end_time):
    return datetime.now().time() < end_time

@register.filter
def gte_time_now(start_time):
    return datetime.now().time() >= start_time