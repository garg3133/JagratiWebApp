from django.urls import path
from . import views

urlpatterns =[
    path('', views.index, name='home'),
    path('dashboard/', views.dashboard, name = 'dashboard'),
    path('set_profile/', views.volunteerInformation, name='set_profile'),
    path('ajax/section_dashboard/', views.showSectionInDashboard, name='show_section_in_dashboard'),
    path('ajax/section_update_schedule/', views.showSectionInUpdateSchedule, name='show_section_in_update_schedule'),
    path('ajax/student_attendence/', views.studentAttendenceAjax, name='student_attendence_ajax'),
]