

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
    path('clients/', views.client_list, name='client_list'),
    path('clients/<int:user_id>/', views.view_client_profile, name='view_client_profile'),
    path('clients/<int:user_id>/diet/', views.edit_diet_plan, name='edit_diet_plan'),
    path('my_diet/', views.view_my_diet_plan, name='view_my_diet'),
    path('announcements/', views.announcements_list, name='announcements_list'),
    path('announcements/create/', views.create_announcement, name='create_announcement'),

]
