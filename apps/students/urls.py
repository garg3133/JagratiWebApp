from django.urls import path

from . import views

app_name = 'students'
urlpatterns = [
    path('', views.index, name='index'),
    path('search/',views.SearchResultsView.as_view(), name='search_results'),
    path('select/<int:select>/',views.SelectClassView.as_view(), name='select_results'),
    path('sort_by/<str:sort_by>/',views.SortNameView.as_view(), name='sort_results'),
    path('new/', views.new_student, name='new_student'),
    path('profile/<int:pk>/', views.profile, name='profile'),
    path('attendance/', views.attendance, name='attendance'),
    path('ajax/attendance/', views.ajax_attendance, name='ajax_attendance'),
    # path('attendance/view/', views.view_attendance, name='view_attendance'),
    path('profile/update/<int:pk>/', views.update_profile, name='update_profile'),  # Not needed, update in profile/ only

    path('update_from_sheets/', views.update_from_sheets, name='update_from_sheets'),
]