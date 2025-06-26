# gym_app/forms.py

from django import forms
from .models import Attendance
from django.contrib.auth.models import User

class AttendanceForm(forms.Form):
    date = forms.DateField(widget=forms.SelectDateWidget)
    clients = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(groups__name='Client'),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
