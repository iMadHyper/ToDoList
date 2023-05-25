from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.views import generic
from . import forms
from . import models

import datetime


def index(request):
    if not request.user.is_authenticated:
        return redirect('users:login')

    form = forms.AddTaskForm()
    tasks = models.Task.objects.filter(user=request.user).filter(is_completed=False).filter(date__lte=datetime.date.today())
    return render(request, 'todo/main.html', { 'form' : form, 'tasks' : tasks})


def add_task(request):
    if not request.user.is_authenticated:
        return redirect('users:login')
    
    if request.method == 'POST':
        form = forms.AddTaskForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cd['user'] = request.user
            models.Task.objects.create(**cd)
            return redirect('app:index')

    else:
        return redirect('app:index')