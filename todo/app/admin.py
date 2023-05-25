from django.contrib import admin

from . import models


@admin.register(models.Category)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(models.Section)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('category', 'name')


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('category', 'section', 'user', 'name', 'description', 'date', 'time', 'is_completed')
    list_filter = ('date', 'time', 'name', 'category', 'section')

    fieldsets = (
        ('Добавить задачу', {
            'description' : 'Основные параметры',
            'fields' : ('user', 'name', 'description', 'date', 'time')
        }),
        ('Дополнительные параметры', {
            'classes' : ('collapse',),
            'fields' : ('category', 'section', 'is_completed')
        }),
    )

    search_fields = ('name', 'description', 'user')
    ordering = ('user', 'name')