from django import forms

from . import models


class TodayTasksFilter(forms.Form):
    name = forms.CharField(
        label='Name',
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class' : 'form-control',
            'placeholder' : 'Name'
        })
    )


class AddTaskForm(forms.ModelForm):
    name = forms.CharField(label='Name', widget=forms.TextInput())
    description = forms.CharField(label='Description', widget=forms.Textarea())
    date = forms.DateField(label='Date', required=False, widget=forms.DateInput())
    time = forms.TimeField(label='Time', required=False, widget=forms.TimeInput())


    class Meta:
        model = models.Task
        fields = ('name', 'description', 'date', 'time')


class AddFolderForm(forms.ModelForm):
    name = forms.CharField(label='Name', widget=forms.TextInput())


    class Meta:
        model = models.Folder
        fields = ('name',)