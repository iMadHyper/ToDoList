from . import models

import datetime


def get_overdue_tasks(user):
    '''Returns user's incompleted overdue tasks'''
    return models.Task.objects.filter(user=user).filter(is_completed=False).filter(date__lt=datetime.date.today()).order_by("-date", "-time")


def get_today_tasks(user):
    '''Returns user's incompleted today tasks'''
    return models.Task.objects.filter(user=user).filter(is_completed=False).filter(date__lte=datetime.date.today()).order_by("-date", "-time")


def get_upcoming_tasks(user):
    '''Returns user's incompleted future tasks'''
    return models.Task.objects.filter(user=user).filter(is_completed=False).filter(date__gt=datetime.date.today()).order_by("-date", "-time")


def get_completed_tasks(user):
    '''Returns user's completed tasks'''
    return models.Task.objects.filter(user=user).filter(is_completed=True).order_by("-date", "-time")


def get_folders(user):
    '''Returns user's folders'''
    return models.Folder.Objects.filter(user=user)


def get_folder_tasks(user, folder_pk):
    '''Returns user's incompleted folder tasks'''
    return models.Folder.objects.filter(user=user).get(pk=folder_pk).get_tasks().filter(is_completed=False).order_by("-date", "-time")