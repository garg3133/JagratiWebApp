from django.urls import path

from . import views

app_name = 'students'
urlpatterns = [
    path('', views.index, name='index'),
    path('profile/<int:pk>/', views.profile, name='profile'),
    path('attendence/', views.attendence, name='attendence'),
    path('ajax/attendence/', views.ajax_attendence, name='ajax_attendence'),
    # path('attendence/view/', views.view_attendence, name='view_attendence'),

    path('update_from_sheets/', views.update_from_sheets, name='update_from_sheets')
]