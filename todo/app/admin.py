from django.contrib import admin

from . import models


@admin.register(models.Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'slug')


@admin.register(models.Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('user', 'folder', 'name')


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'description', 'date', 'time', 'is_completed')
    list_filter = ('date', 'time', 'name', 'folder', 'section')

    fieldsets = (
        ('Добавить задачу', {
            'description' : 'Основные параметры',
            'fields' : ('user', 'name', 'description', 'date', 'time')
        }),
        ('Дополнительные параметры', {
            'classes' : ('collapse',),
            'fields' : ('folder', 'section', 'is_completed')
        }),
    )

    search_fields = ('name', 'description', 'user')
    ordering = ('user', 'name')