from django.db import models

import datetime


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(max_length=500, verbose_name='Описание')


    def __str__(self):
        return self.name
    

    def get_sections(self):
        return self.sections.all()
    

    def get_tasks(self):
        return self.tasks.all()


class Section(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='sections')
    name = models.CharField(max_length=100, verbose_name='Название')


    def __str__(self):
        return self.name
    

    def get_tasks(self):
        return self.tasks.all()


class Task(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='tasks')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='tasks')
    name = models.CharField(max_length=150, verbose_name='Название')
    description = models.TextField(max_length=500, verbose_name='Описание')
    date = models.DateField(verbose_name='Дата', default=datetime.date.today)
    time = models.TimeField(verbose_name='Время', null=True, blank=True)
    is_completed = models.BooleanField(default=False, verbose_name='Выполнена')

    class Meta:
        verbose_name = 'task'
        verbose_name_plural = 'tasks'


    def __str__(self):
        return self.name