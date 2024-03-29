from django.db import models

from django.contrib.auth.models import User

import datetime


class Folder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='folders', verbose_name='Пользователь', null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name='Название')

    def __str__(self):
        return self.name
    

    def get_sections(self):
        return self.sections.all()
    

    def get_tasks(self):
        return self.tasks.all()


class Task(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.SET_NULL, related_name='tasks', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks', verbose_name='Пользователь', null=True, blank=True)
    name = models.CharField(max_length=150, verbose_name='Название')
    description = models.TextField(max_length=500, verbose_name='Описание', null=True, blank=True)
    date = models.DateField(verbose_name='Дата', default=datetime.date.today)
    time = models.TimeField(verbose_name='Время', null=True, blank=True)
    is_completed = models.BooleanField(default=False, verbose_name='Выполнена')

    class Meta:
        verbose_name = 'task'
        verbose_name_plural = 'tasks'


    def __str__(self):
        return self.name