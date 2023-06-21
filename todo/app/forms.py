from django import forms

from . import models
from . import actions


class TodayTasksFilter(forms.Form):
    name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class' : 'form-control fs-4',
            'placeholder' : 'Name'
        })
    )
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