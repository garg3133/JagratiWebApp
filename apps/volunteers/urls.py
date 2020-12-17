from django.urls import path

from . import views

app_name = 'volunteers'
urlpatterns = [
    path('', views.index, name='index'),
    path('profile/<int:pk>/', views.profile, name='profile'),
    path('attendance/', views.attendance, name='attendance'),
    # path('attendance/view/', views.view_attendance, name='view_attendance'),
    path('update_schedule/', views.update_schedule, name='update_schedule'),
    path('ajax/update_schedule/', views.ajax_update_schedule, name='ajax_update_schedule'),

    # Needs to be changed
    path('profile/update/', views.update_profile, name='update_profile'),  # Not needed, update in profile/ only
    path('list/', views.volunteers_list, name='volunteers_list'),
    path('ajax/list/', views.ajax_volunteers_list, name='ajax_volunteers_list'),
    path('all_volunteers/', views.VolunteerListView.as_view(), name='all_volunteers'),
]