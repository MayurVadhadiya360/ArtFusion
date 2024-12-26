from django import template
from datetime import datetime
from django.utils.timezone import now

register = template.Library()

@register.filter
def custom_timesince(created_at:datetime):
    diff = now() - created_at

    seconds = diff.total_seconds()
    minutes = seconds // 60
    hours = minutes // 60
    days = hours // 24
    weeks = days // 7
    months = days // 30
    years = months // 12

    if seconds < 60:
        return "Now"
    elif minutes < 60:
        return f"{int(minutes)}m"
    elif hours < 24:
        return f"{int(hours)}h"
    elif days < 7:
        return f"{int(days)}d"
    elif months < 12:
        return f"{int(weeks)}w"
    else:
        return f"{int(years)}y"
