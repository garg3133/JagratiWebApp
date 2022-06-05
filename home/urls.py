from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new_index, name='new_index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/update_cwhw/', views.update_cwhw, name='update_cwhw'),
    path('ajax/dashboard/', views.ajax_dashboard, name='ajax_dashboard'),
    path('dashboard/class_schedule/', views.class_schedule, name='class_schedule'),
    path('calendar/', views.calendar, name='calendar'),
    path('ajax/fetch_calendar', views.ajax_fetch_calendar, name='ajax_fetch_calendar'),
]
