from django.urls import path

from . import views

app_name = 'volunteers'
urlpatterns = [
    path('', views.index, name='index'),
    path('profile/<int:pk>/', views.profile, name='profile'),
    path('attendence/', views.attendence, name='attendence'),
    # path('attendence/view/', views.view_attendence, name='view_attendence'),

    # Needs to be changed
    # path('profile/update/', views.updateProfile, name='update_profile'),  # Not needed, update in profile/ only
    # path('volList/', views.volunteersList, name='vol_list'),
    # path('ajax/volunteer_list/', views.volunteerListAjax, name='volunteer_list_ajax'),
]