from django import template

from app import models
from app import forms

import datetime

from app import actions


register = template.Library()


@register.simple_tag()
def get_overdue_tasks(user):
    return actions.get_overdue_tasks(user)


@register.simple_tag()
def get_today_tasks(user):
    return actions.get_today_tasks(user)


@register.simple_tag()
def get_completed_tasks(user):
    return actions.get_completed_tasks(user)


@register.simple_tag()
def get_upcoming_tasks(user):
    return actions.get_upcoming_tasks(user)


@register.simple_tag()
def get_folders(user):
    return actions.get_folders(user)


@register.simple_tag()
def get_folder_form():
    return forms.AddFolderForm()


@register.simple_tag()
def get_folder_tasks(user, folder_pk):
    return actions.get_folder_tasks(user, folder_pk)