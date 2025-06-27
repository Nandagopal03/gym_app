# gym_app/forms.py

from django import forms 
from .models import Attendance, Fee, ClientProfile, DietPlan, Announcement
from django.contrib.auth.models import User

class AttendanceForm(forms.Form):
    date = forms.DateField(widget=forms.SelectDateWidget)
    clients = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(groups__name='Client'),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )


class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = ClientProfile
        fields = [
            'profile_photo', 'full_name', 'gender', 'age',
            'phone', 'alt_phone', 'address',
            'height', 'weight', 'medical_condition'
        ]
        widgets = {
            'gender': forms.Select(choices=[('', 'Select Gender')] + list(ClientProfile._meta.get_field('gender').choices)),
            'address': forms.Textarea(attrs={'rows': 2}),
            'medical_condition': forms.Textarea(attrs={'rows': 2}),
        }
        
        


class DietPlanForm(forms.ModelForm):
    class Meta:
        model = DietPlan
        fields = ['morning', 'afternoon', 'evening', 'night']
        widgets = {
            'morning': forms.Textarea(attrs={'rows': 2}),
            'afternoon': forms.Textarea(attrs={'rows': 2}),
            'evening': forms.Textarea(attrs={'rows': 2}),
            'night': forms.Textarea(attrs={'rows': 2}),
        }

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'message']