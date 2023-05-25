from django import forms

from . import models


class AddTaskForm(forms.ModelForm):
    class Meta:
        model = models.Task
        fields = ('name', 'description', 'date', 'time')
        widgets = {
            'name' : forms.TextInput(attrs={'class' : 'form-input'}),
            'description' : forms.Textarea(attrs={'cols' : 60, 'rows' : 2}),
            'date' : forms.DateInput(),
            'time' : forms.TimeInput()
        }