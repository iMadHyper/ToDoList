from django import template

from app import models

import datetime


register = template.Library()


@register.simple_tag()
def get_today_tasks(user):
    return models.Task.objects.filter(user=user).filter(is_completed=False).filter(date__lte=datetime.date.today()).order_by("-date", "-time")


@register.simple_tag()
def get_completed_tasks(user):
    return models.Task.objects.filter(user=user).filter(is_completed=True).order_by("-date", "-time")


@register.simple_tag()
def get_upcoming_tasks(user):
    return models.Task.objects.filter(user=user).filter(is_completed=False).filter(date__gt=datetime.date.today()).order_by("-date", "-time")