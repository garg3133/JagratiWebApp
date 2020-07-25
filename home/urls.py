from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('ajax/dashboard/', views.ajax_dashboard, name='ajax_dashboard'),
]