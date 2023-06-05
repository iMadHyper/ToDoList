from django import forms

from . import models


class AddTaskForm(forms.ModelForm):
    name = forms.CharField(label='Name', widget=forms.TextInput())
    description = forms.CharField(label='Description', widget=forms.Textarea())
    date = forms.DateField(label='Date', required=False, widget=forms.DateInput())
    time = forms.TimeField(label='Time', required=False, widget=forms.TimeInput())


    class Meta:
        model = models.Task
        fields = ('name', 'description', 'date', 'time')