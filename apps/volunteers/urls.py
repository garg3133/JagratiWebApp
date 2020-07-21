from django.urls import path

from . import views

app_name = 'volunteers'
urlpatterns = [
    path('', views.index, name='index'),
    path('profile/<int:pk>/', views.profile, name='profile'),
    path('attendence/', views.attendence, name='attendence'),
    # path('attendence/view/', views.view_attendence, name='view_attendence'),

    # Needs to be changed
    path('profile/update/', views.update_profile, name='update_profile'),  # Not needed, update in profile/ only
    path('list/', views.volunteers_list, name='volunteers_list'),
    path('ajax/list/', views.ajax_volunteers_list, name='ajax_volunteers_list'),
]