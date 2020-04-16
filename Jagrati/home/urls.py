from django.urls import path
from . import views

urlpatterns =[
    path('', views.index, name='home'),
    path('dashboard/', views.dashboard, name = 'dashboard'),
    path('set_profile/', views.completeProfile, name='set_profile'),
    path('feedback/', views.feedback, name = 'feedback'),
    path('ajax/section_dashboard/', views.showSectionInDashboard, name='show_section_in_dashboard'),
    path('ajax/section_update_schedule/', views.showSectionInUpdateSchedule, name='show_section_in_update_schedule'),
    path('ajax/student_attendence/', views.studentAttendenceAjax, name='student_attendence_ajax'),
    path('ajax/volunteer_list/', views.volunteerListAjax, name='volunteer_list_ajax'),

    path('update_students/', views.update_students, name='update_students'),


    path('stuAtt/', views.studentsAttendence, name='stu_attendence'),
    path('volAtt/', views.volunteersAttendence, name='vol_attendence'),
]