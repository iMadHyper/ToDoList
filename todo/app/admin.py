from django.contrib import admin

from . import models


@admin.register(models.Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = ('user', 'name')


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'description', 'date', 'time', 'is_completed')
    list_filter = ('date', 'time', 'name', 'folder')

    fieldsets = (
        ('Добавить задачу', {
            'description' : 'Основные параметры',
            'fields' : ('user', 'name', 'description', 'date', 'time')
        }),
        ('Дополнительные параметры', {
            'classes' : ('collapse',),
            'fields' : ('folder', 'is_completed')
        }),
    )

    search_fields = ('name', 'description', 'user')
    ordering = ('user', 'name')