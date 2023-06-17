from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.text import slugify

from . import forms
from . import models

import datetime

import re


def if_logged_in(func):
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
                messages.success(request, 'Date can\'t be past!')
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


def respect_redirect_after_adding_task(request):
    '''
    Redirect to template from request if possible
    '''
    url = '/'.join(request.META['HTTP_REFERER'].split('//')[1].split('/')[1:])
    print(url)
    if url == 'app/upcoming/':
        return redirect('app:upcoming_tasks')
    else:
        return redirect('app:index')
    

def respect_render_after_adding_task(request, msg=None):
    '''
    Render the template from request if possible
    '''
    url = '/'.join(request.META['HTTP_REFERER'].split('//')[1].split('/')[1:])
    if url == 'app/upcoming/':
        return render(request, 'todo/upcoming_tasks.html', { 'msg' : msg })
    else:
        return render(request, 'todo/main.html', { 'msg' : msg })


@if_logged_in
def add_task(request):
    if request.method == 'POST':
        form = forms.AddTaskForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cd['user'] = request.user
            print(cd['time'])

            if not cd['date']:
                cd['date'] = datetime.date.today()
            elif cd['date'] < datetime.date.today():
                msg = 'Date can\'t be past!'
                return respect_render_after_adding_task(request, msg=msg)
            
            if cd['time']:
                now = datetime.datetime.now()
                t1 = datetime.timedelta(hours=cd['time'].hour, minutes=cd['time'].minute, seconds=cd['time'].second)
                t2 = datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second)
                if t1 < t2:
                    msg = 'Date and time can\'t be past!'
                    return respect_render_after_adding_task(request, msg=msg)
            
            models.Task.objects.create(**cd)
            return respect_redirect_after_adding_task(request)
        
        else:
            return respect_render_after_adding_task(request, msg=form.errors)
    else:
        try:
            return redirect(request.META['HTTP_REFERER'])
        except:
            return redirect('app:index')


@if_logged_in
def delete_task(request, pk):
    task = models.Task.objects.filter(user=request.user).get(pk=pk)

    if task:
        task.delete()

    try:
        return redirect(request.META['HTTP_REFERER'])
    except:
        return redirect('app:index')


@if_logged_in
def complete_task(request, pk):
    task = models.Task.objects.filter(user=request.user).get(pk=pk)

    if task:
        task.is_completed = True
        task.save()

    try:
        return redirect(request.META['HTTP_REFERER'])
    except:
        return redirect('app:index')


@if_logged_in
def completed_tasks(request):
    return render(request, 'todo/completed_tasks.html')


@if_logged_in
def upcoming_tasks(request):
    form = forms.AddTaskForm()

    return render(request, 'todo/upcoming_tasks.html', { 'form' : form })


redirects = {
    'app/today/' : 'app:index',
    'app/upcoming/' : 'app:upcoming_tasks',
    'app/completed/' : 'app:completed_tasks',
}

renders = {

}

def respect_redirect(request):
    '''
    Redirect to template from request if possible
    '''
    url = '/'.join(request.META['HTTP_REFERER'].split('//')[1].split('/')[1:]).strip()
    print(url)
    try:
        if re.match(r'^app/(\d+)/$', url):
            print('true')
            print(url.split('/')[1])
            try:
                return redirect('app:folder_tasks', folder_pk=int(url.split('/')[1]))
            except:
                return redirect('app:index')
        return redirect(redirects[url])
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
            return respect_redirect(request)
    else:
        return respect_redirect(request)


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