from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),   # Landing Page
    path('setprofile/', views.completeProfile, name='set_profile'),   # Complete your Profile Page

    path('dashboard/', views.dashboard, name = 'dashboard'),   # Dashboard
    path('ajax/section_dashboard/', views.showSectionInDashboard, name='show_section_in_dashboard'),

    path('updateSchedule/', views.updateSchedule, name='update_schedule'),   # Update Schedule
    path('ajax/section_update_schedule/', views.showSectionInUpdateSchedule, name='show_section_in_update_schedule'),

    path('updateProfile/', views.updateProfile, name='update_profile'),   # Update Profile

    path('stuAtt/', views.studentsAttendence, name='stu_attendence'),   # Students Attendence
    path('ajax/student_attendence/', views.studentAttendenceAjax, name='student_attendence_ajax'),

    path('volAtt/', views.volunteersAttendence, name='vol_attendence'),   # Volunteers Attendence

    path('volList/', views.volunteersList, name='vol_list'),   # Volunteers List
    path('ajax/volunteer_list/', views.volunteerListAjax, name='volunteer_list_ajax'),

    path('feedback/', views.feedback, name = 'feedback'),   # Feedback Page
    path('update_students/', views.update_students, name='update_students'),   # Update Students from Spreadsheet Script

]