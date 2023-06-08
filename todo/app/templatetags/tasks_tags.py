from django import template

from app import models
from app import forms

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


@register.simple_tag()
def get_folders(user):
    return models.Folder.objects.filter(user=user)


@register.simple_tag()
def get_folder_form():
    return forms.AddFolderForm()


@register.simple_tag()
def get_folder_tasks(user, folder_pk):
    return models.Folder.objects.filter(user=user).get(pk=folder_pk).get_tasks().filter(is_completed=False)