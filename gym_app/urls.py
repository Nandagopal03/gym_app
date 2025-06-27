

from django.urls import path
from . import views

urlpatterns = [
    path('', views.custom_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('mark_attendance/', views.mark_attendance, name='mark_attendance'),
    path('view_attendance/', views.view_attendance, name='view_attendance'),
    path('all_fees/', views.view_all_fees, name='view_all_fees'),
    path('view_fees/', views.view_fees, name='view_fees'),
    path('profile/view/', views.view_profile, name='view_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),




]
