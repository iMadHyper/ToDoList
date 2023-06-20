from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.text import slugify

from django.core.exceptions import ObjectDoesNotExist

from . import forms
from . import models

import datetime


# Renders errors passsed in messages
ERRORS_TEMPLATE = 'todo/errors.html'


def if_logged_in(func):
    '''
    Redirects the user to login page if he's not logged in
    '''
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('users:login')
        return func(request, *args, **kwargs)
    return wrapper


@if_logged_in
def index(request):
    template_name = 'todo/main.html'

    if request.method == 'POST':
        form = forms.AddTaskForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cd['user'] = request.user

            if not cd['date']:
                cd['date'] = datetime.date.today()
            elif cd['date'] < datetime.date.today():
                messages.success(request, 'Date and time can\'t be past!')
                return render(request, template_name)

            if cd['time']:
                now = datetime.datetime.now()
                t1 = datetime.timedelta(hours=cd['time'].hour, minutes=cd['time'].minute, seconds=cd['time'].second)
                t2 = datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second)
                if t1 < t2:
                    messages.success(request, 'Date and time can\'t be past!')
                    return render(request, template_name)
            
            models.Task.objects.create(**cd)
            return render(request, template_name)
        else:
            messages.success(request, f'{form.errors}')
            return render(request, template_name)
    else:
        form = forms.AddTaskForm()
        return render(request, template_name, { 'form' : form })


@if_logged_in
def upcoming_tasks(request):
    template_name = 'todo/upcoming_tasks.html'
    if request.method == 'POST':
        form = forms.AddTaskForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cd['user'] = request.user

            if not cd['date']:
                cd['date'] = datetime.date.today()
            elif cd['date'] < datetime.date.today():
                messages.success(request, 'Date and time can\'t be past!')
                return render(request, template_name)

            if cd['time']:
                now = datetime.datetime.now()
                t1 = datetime.timedelta(hours=cd['time'].hour, minutes=cd['time'].minute, seconds=cd['time'].second)
                t2 = datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second)
                if t1 < t2:
                    messages.success(request, 'Date and time can\'t be past!')
                    return render(request, template_name)
            
            models.Task.objects.create(**cd)
            return render(request, template_name)
        else:
            messages.success(request, f'{form.errors}')
            return render(request, template_name)
    else:
        form = forms.AddTaskForm()
        return render(request, template_name, { 'form' : form })


@if_logged_in
def completed_tasks(request):
    return render(request, 'todo/completed_tasks.html')


@if_logged_in
def overdue_tasks(request):
    return render(request, 'todo/overdue_tasks.html')


@if_logged_in
def delete_task(request, pk):
    try:
        task = models.Task.objects.filter(user=request.user).filter(is_completed=False).get(pk=pk)
    except:
        messages.success(request, 'The task matching query does not exist!')
        return render(request, ERRORS_TEMPLATE)

    task.delete()

    try:
        return redirect(request.META['HTTP_REFERER'])
    except:
        return redirect('app:index')


@if_logged_in
def complete_task(request, pk):
    try:
        task = models.Task.objects.filter(user=request.user).filter(is_completed=False).get(pk=pk)
    except ObjectDoesNotExist:
        messages.success(request, 'The task matching query does not exist!')
        return render(request, ERRORS_TEMPLATE)

    task.is_completed = True
    task.save()

    try:
        return redirect(request.META['HTTP_REFERER'])
    except:
        return redirect('app:index')


@if_logged_in
def add_folder(request):
    if request.method == 'POST':
        form = forms.AddFolderForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cd['user'] = request.user
            folder = models.Folder.objects.create(**cd)
            return redirect('app:folder_tasks', folder_pk=folder.id)
        else:
            messages.success(request, 'The form is not valid!')
            return render(request, ERRORS_TEMPLATE)
    else:
        return redirect('app:index')


@if_logged_in
def delete_folder(request, pk):
    try:
        folder = models.Folder.objects.filter(user=request.user).get(pk=pk)
    except:
        messages.success(request, 'The folder matching query does not exist!')
        return render(request, ERRORS_TEMPLATE)

    folder_tasks = folder.get_tasks()
    if folder_tasks:
        folder_tasks.delete()
    folder.delete()

    return redirect('app:index')


@if_logged_in
def folder_tasks(request, folder_pk):
    template_name = 'todo/folder_tasks.html'

    try:
        folder = models.Folder.objects.filter(user=request.user).get(pk=folder_pk)
    except:
        messages.success(request, 'The folder matching query does not exist!')
        return render(request, ERRORS_TEMPLATE)

    if request.method == 'POST':
        form = forms.AddTaskForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cd['user'] = request.user
            cd['folder'] = folder

            if not cd['date']:
                cd['date'] = datetime.date.today()
            elif cd['date'] < datetime.date.today():
                messages.success(request, 'Date and time can\'t be past!')
                return render(request, template_name, { 'folder' : folder })
            
            if cd['time']:
                now = datetime.datetime.now()
                t1 = datetime.timedelta(hours=cd['time'].hour, minutes=cd['time'].minute, seconds=cd['time'].second)
                t2 = datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second)
                if t1 < t2:
                    messages.success(request, 'Date and time can\'t be past!')
                    return render(request, template_name, { 'folder' : folder })
            
            models.Task.objects.create(**cd)
            return render(request, template_name, { 'folder' : folder })
        else:
            messages.success(request, f'{form.errors}')
            return render(request, template_name, { 'folder' : folder })
    else:
        form = forms.AddTaskForm()
        return render(request, template_name, { 'folder' : folder, 'form' : form })