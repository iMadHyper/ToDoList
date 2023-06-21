from django import forms

from . import models
from . import actions


class TasksFilter(forms.Form):
    name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class' : 'form-control fs-4',
            'placeholder' : 'Name'
        })
    )


class TasksFilterWithFolder(TasksFilter):
    folder = forms.ModelChoiceField(
        queryset=None,
        label='Folder',
        required=False,
        empty_label='Folder',
        widget=forms.Select(attrs={
            'class' : 'form-select fs-4'
        })
    )


    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['folder'].queryset = actions.get_folders(user)


class TasksFilterWithDate(TasksFilter):
    date_start = forms.DateField(
        required=False,
        label='Start date',
        widget=forms.DateInput(attrs={
            'class' : 'form-control fs-4',
            'placeholder' : 'Start date',
            'type' : 'date'
        })
    )

    date_end = forms.DateField(
        required=False,
        label='End date',
        widget=forms.DateInput(attrs={
            'class' : 'form-control fs-4',
            'placeholder' : 'End date',
            'type' : 'date'
        })
    )


class TasksFilterWithDateAndFolder(TasksFilterWithDate, TasksFilterWithFolder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class AddTaskForm(forms.ModelForm):
    name = forms.CharField(label='Name', widget=forms.TextInput())
    description = forms.CharField(label='Description', required=False, widget=forms.Textarea())
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