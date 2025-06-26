# gym_app/admin.py

from django.contrib import admin
from .models import Attendance, Fee

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('client', 'date', 'present')
    list_filter = ('date', 'present')


@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ('client', 'amount', 'paid', 'date', 'due_date')
    list_filter = ('paid', 'due_date')
