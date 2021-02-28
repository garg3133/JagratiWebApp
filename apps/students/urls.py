from django.urls import path

from . import views

app_name = 'students'
urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new_student, name='new_student'),
    path('profile/<int:pk>/', views.profile, name='profile'),
    path('attendance/', views.attendance, name='attendance'),
    # path('attendance/view/', views.view_attendance, name='view_attendance'),
    path('profile/update/<int:pk>/', views.update_profile, name='update_profile'),  # Not needed, update in profile/ only

    path('update_from_sheets/', views.update_from_sheets, name='update_from_sheets'),

    # AJAX calls
    path('ajax/fetch_students/', views.ajax_fetch_students, name='ajax_fetch_students'),
    path('ajax/mark_attendance/', views.ajax_mark_attendance, name='ajax_mark_attendance'),

]