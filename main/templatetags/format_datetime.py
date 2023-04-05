from django import template
import datetime
from django.utils import timezone
register = template.Library()


@register.filter
def format_datetime(datetime):
    return f'{datetime.astimezone(timezone.get_current_timezone()).strftime("%d.%m.%Y")} на {datetime.astimezone(timezone.get_current_timezone()).strftime("%H:%M")}'