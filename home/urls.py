from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.new_index, name='new_index'),
    path('old/', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/update_cwhw/', views.update_cwhw, name='update_cwhw'),
    path('ajax/dashboard/', views.ajax_dashboard, name='ajax_dashboard'),
]