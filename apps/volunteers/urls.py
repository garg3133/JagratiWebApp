from django.urls import path

from . import views

app_name = 'volunteers'
urlpatterns = [
    path('', views.index, name='index'),
    path('profile/<int:pk>/', views.profile, name='profile'),
    path('attendance/', views.attendance, name='attendance'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    # path('attendance/view/', views.view_attendance, name='view_attendance'),
    path('update_schedule/', views.update_schedule, name='update_schedule'),
    path('ajax/update_schedule/', views.ajax_update_schedule, name='ajax_update_schedule'),

    # Needs to be changed
    path('profile/update/', views.update_profile, name='update_profile'),  # Not needed, update in profile/ only
    path('list/', views.volunteers_list, name='volunteers_list'),
    path('ajax/list/', views.ajax_volunteers_list, name='ajax_volunteers_list'),

    # AJAX calls
    path('ajax/mark_attendance/', views.ajax_mark_attendance, name='ajax_mark_attendance'),
    path('ajax/add_extra_vol/', views.ajax_add_extra_vol, name='ajax_add_extra_vol'),
]