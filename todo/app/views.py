from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.text import slugify

from . import forms
from . import models

import datetime


def if_logged_in(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('users:login')
        return func(request, *args, **kwargs)
    return wrapper


@if_logged_in
def index(request):
    form = forms.AddTaskForm()
    
    return render(request, 'todo/main.html', { 'form' : form })


@if_logged_in
def add_task(request):
    if request.method == 'POST':
        form = forms.AddTaskForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cd['user'] = request.user
            if not cd['date']:
                cd['date'] = datetime.date.today()
            models.Task.objects.create(**cd)
            return redirect('app:index')
        else:
            messages.success(request, f'{form.errors}')
            return render(request, 'todo/main.html')
    else:
        return redirect('app:index')


@if_logged_in
def delete_task(request, pk):
    task = models.Task.objects.filter(user=request.user).get(pk=pk)

    if task:
        task.delete()

    return redirect(request.META['HTTP_REFERER'])


@if_logged_in
def complete_task(request, pk):
    task = models.Task.objects.filter(user=request.user).get(pk=pk)

    if task:
        task.is_completed = True
        task.save()

    return redirect(request.META['HTTP_REFERER'])


@if_logged_in
def completed_tasks(request):
    return render(request, 'todo/completed_tasks.html')


@if_logged_in
def upcoming_tasks(request):
    form = forms.AddTaskForm()

    return render(request, 'todo/upcoming_tasks.html', { 'form' : form })


@if_logged_in
def add_folder(request):
    if request.method == 'POST':
        form = forms.AddFolderForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cd['user'] = request.user
            cd['slug'] = slugify(str(cd['name']))
            models.Folder.objects.create(**cd)
            return redirect(request.META['HTTP_REFERER'])
        else:
            return redirect(request.META['HTTP_REFERER'])
    else:
        return redirect('app:index')


@if_logged_in
def delete_folder(request, pk):
    folder = models.Folder.objects.filter(user=request.user).get(pk=pk)
    folder_tasks = folder.get_tasks()

    if folder_tasks:
        folder_tasks.delete()

    if folder:
        folder.delete()

    return redirect('app:index')


@if_logged_in
def folder_tasks(request, folder_pk):
    folder = models.Folder.objects.filter(user=request.user).get(pk=folder_pk)

    if not folder:
        return redirect(request.META['HTTP_REFERER'])
    
    return render(request, 'todo/folder_tasks.html', { 'folder' : folder })


@if_logged_in
def add_folder_task(request, folder_pk):
    folder = models.Folder.objects.filter(user=request.user).get(pk=folder_pk)

    if not folder:
        return redirect(request.META['HTTP_REFERER'])
    
    if request.method == 'POST':
        form = forms.AddTaskForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cd['user'] = request.user
            cd['folder'] = folder
            if not cd['date']:
                cd['date'] = datetime.date.today()
            models.Task.objects.create(**cd)
            return redirect('app:folder_tasks', folder_pk=folder.id)
        else:
            messages.success(request, f'{form.errors}')
            return redirect('app:folder_tasks', folder_pk=folder.id)
    else:
        return redirect('app:index')