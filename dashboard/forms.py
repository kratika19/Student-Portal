from django import forms
from django.forms import widgets

from .models import *


class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title', 'description']


class DateInput(forms.DateInput):
    input_type = 'date'


class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        widgets = {'due_date': DateInput()}
        exclude = ['user']


class DashboardForm(forms.Form):
    text = forms.CharField(max_length=500, label='Enter Your Search')


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'status']
