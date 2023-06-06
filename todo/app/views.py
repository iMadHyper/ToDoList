from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.views import generic
from . import forms
from . import models

from django.contrib import messages

import datetime


def index(request):
    if not request.user.is_authenticated:
        return redirect('users:login')

    form = forms.AddTaskForm()
    
    return render(request, 'todo/main.html', { 'form' : form })


def add_task(request):
    if not request.user.is_authenticated:
        return redirect('users:login')
    
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


def delete_task(request, pk):
    if not request.user.is_authenticated:
        return redirect('users:login')
    
    task = models.Task.objects.filter(user=request.user).get(pk=pk)

    if task:
        task.delete()

    return redirect(request.META['HTTP_REFERER'])


def complete_task(request, pk):
    if not request.user.is_authenticated:
        return redirect('users:login')
    
    task = models.Task.objects.filter(user=request.user).get(pk=pk)

    if task:
        task.is_completed = True
        task.save()

    return redirect(request.META['HTTP_REFERER'])


def completed_tasks(request):
    if not request.user.is_authenticated:
        return redirect('users:login')
    
    return render(request, 'todo/completed_tasks.html')


def upcoming_tasks(request):
    if not request.user.is_authenticated:
        return redirect('users:login')
    
    form = forms.AddTaskForm()

    return render(request, 'todo/upcoming_tasks.html', { 'form' : form })


def add_folder(request):
    if not request.user.is_authenticated:
        return redirect('users:login')
    
    if request.method == 'POST':
        form = forms.AddFolderForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cd['user'] = request.user
            models.Folder.objects.create(**cd)
            return redirect(request.META['HTTP_REFERER'])
        else:
            return redirect(request.META['HTTP_REFERER'])
    else:
        return redirect('app:index')


def delete_folder(request, pk):
    if not request.user.is_authenticated:
        return redirect('users:login')
    
    folder = models.Folder.objects.filter(user=request.user).get(pk=pk)

    if folder:
        folder.delete()

    return redirect(request.META['HTTP_REFERER'])